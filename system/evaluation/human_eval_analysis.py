"""Analysis for the human evaluation survey (SOT §19.3; PLAN §6.3).

*** Cannot run until real survey responses exist. Do not fabricate input
data for this script -- it is meant to run on genuine participant
responses only. ***

Expects a long-format CSV of real responses with columns:
  participant_id, video_id, blinded_label, dimension, rating
where blinded_label is one of "title_1"/"title_2"/"title_3" (matching
human_eval_stimulus.csv) and dimension is one of curiosity /
emotional_impact / clarity / trustworthiness (SOT §19.3's rubric). Most
survey tools (Google Forms, Typeform) export one row per respondent with
one column per question -- reshape that wide export into this long format
before running this script; the exact reshape depends on the tool used, so
it isn't automated here.

Joins responses against human_eval_answer_key.csv (produced by
human_eval_stimulus.py) to recover which condition (baseline_a /
baseline_b / system) each blinded_label actually was, then:
  - computes mean rating per condition per dimension
  - runs a paired Wilcoxon signed-rank test, System vs each baseline, per
    dimension (matches PLAN §6.3's "Wilcoxon signed-rank test or t-test")
  - computes Pearson r between human "curiosity" ratings and the LLM
    judge's "curiosity" scores (system/evaluation/outputs/llm_judge_results.json)
    for the same (video_id, condition) pairs -- the one rubric dimension
    that's directly comparable between SOT §19.3's human rubric and
    §19.4's judge rubric -- as the inter-rater reliability check §19.4 asks for.

Usage: python -m system.evaluation.human_eval_analysis path/to/responses.csv
"""

import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from scipy import stats

OUT_DIR = Path(__file__).resolve().parent / "outputs"
RUBRIC_DIMENSIONS = ["curiosity", "emotional_impact", "clarity", "trustworthiness"]


def load_answer_key():
    key = {}
    with open(OUT_DIR / "human_eval_answer_key.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key[(int(row["video_id"]), row["blinded_label"])] = row["condition"]
    return key


def load_responses(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "participant_id": row["participant_id"],
                    "video_id": int(row["video_id"]),
                    "blinded_label": row["blinded_label"],
                    "dimension": row["dimension"],
                    "rating": float(row["rating"]),
                }
            )
    return rows


def analyze(responses_path):
    answer_key = load_answer_key()
    responses = load_responses(responses_path)

    # (condition, dimension) -> list[rating]
    by_condition_dim = defaultdict(list)
    # (participant_id, video_id, dimension) -> {condition: rating}, for pairing
    paired = defaultdict(dict)
    # (video_id, condition) -> list[curiosity rating], for LLM-judge reliability
    curiosity_by_video_condition = defaultdict(list)

    for r in responses:
        condition = answer_key.get((r["video_id"], r["blinded_label"]))
        if condition is None:
            continue
        by_condition_dim[(condition, r["dimension"])].append(r["rating"])
        paired[(r["participant_id"], r["video_id"], r["dimension"])][condition] = r["rating"]
        if r["dimension"] == "curiosity":
            curiosity_by_video_condition[(r["video_id"], condition)].append(r["rating"])

    means = {
        condition: {
            dim: statistics.mean(by_condition_dim[(condition, dim)])
            for dim in RUBRIC_DIMENSIONS
            if by_condition_dim[(condition, dim)]
        }
        for condition in ("baseline_a", "baseline_b", "system")
    }

    significance = {}
    for baseline in ("baseline_a", "baseline_b"):
        significance[f"system_vs_{baseline}"] = {}
        for dim in RUBRIC_DIMENSIONS:
            sys_vals, base_vals = [], []
            for key, conditions in paired.items():
                if key[2] != dim:
                    continue
                if "system" in conditions and baseline in conditions:
                    sys_vals.append(conditions["system"])
                    base_vals.append(conditions[baseline])
            if len(sys_vals) < 2:
                significance[f"system_vs_{baseline}"][dim] = {"note": "insufficient paired data"}
                continue
            diffs = [s - b for s, b in zip(sys_vals, base_vals)]
            if all(d == 0 for d in diffs):
                significance[f"system_vs_{baseline}"][dim] = {
                    "statistic": None, "p_value": None, "note": "no difference"
                }
                continue
            result = stats.wilcoxon(sys_vals, base_vals)
            significance[f"system_vs_{baseline}"][dim] = {
                "n_pairs": len(sys_vals),
                "statistic": float(result.statistic),
                "p_value": float(result.pvalue),
            }

    reliability = _curiosity_reliability(curiosity_by_video_condition)

    summary = {
        "n_responses": len(responses),
        "mean_scores_by_condition": means,
        "significance": significance,
        "llm_judge_reliability_curiosity_pearson_r": reliability,
    }
    print(json.dumps(summary, indent=2))
    with open(OUT_DIR / "human_eval_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved -> {OUT_DIR / 'human_eval_results.json'}")


def _curiosity_reliability(curiosity_by_video_condition):
    """Pearson r between mean human curiosity rating and the LLM judge's
    curiosity score, paired by (video_id, condition). video_id here is the
    1-indexed position assigned in human_eval_stimulus.py, which reads the
    same llm_judge_results.json in the same order -- so video_id N here
    corresponds to per_video[N-1] there. This is the one rubric dimension
    SOT §19.3 (human) and §19.4 (LLM judge) share directly, so it's the
    only one usable for inter-rater reliability without redefining either
    rubric.
    """
    judge_path = OUT_DIR / "llm_judge_results.json"
    if not judge_path.exists():
        return {"error": "llm_judge_results.json not found -- run llm_judge_eval.py first"}
    with open(judge_path) as f:
        judge_per_video = json.load(f)["per_video"]

    human_means, judge_scores = [], []
    for (video_id, condition), ratings in curiosity_by_video_condition.items():
        video_index = video_id - 1
        if not (0 <= video_index < len(judge_per_video)):
            continue
        judge_curiosity = judge_per_video[video_index]["scores"].get(condition, {}).get("curiosity")
        if judge_curiosity is None or not ratings:
            continue
        human_means.append(statistics.mean(ratings))
        judge_scores.append(judge_curiosity)

    if len(human_means) < 3:
        return {"error": f"only {len(human_means)} paired (video, condition) points -- need >= 3"}

    r, p_value = stats.pearsonr(human_means, judge_scores)
    return {"n_pairs": len(human_means), "pearson_r": float(r), "p_value": float(p_value)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m system.evaluation.human_eval_analysis path/to/responses.csv")
        sys.exit(1)
    analyze(sys.argv[1])
