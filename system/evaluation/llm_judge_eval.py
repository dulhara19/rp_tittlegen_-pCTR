"""LLM-as-a-Judge orchestration (SOT §19.4; PLAN §6.4).

Runs all 20 video inputs (system/evaluation/eval_video_inputs.py) through:
  - the full Analyzer -> Generator -> Critic pipeline for the System condition
  - Baseline A (descriptive stand-in) and Baseline B (zero-shot LLM)
then judges all 3 conditions x 20 videos = 60 evaluations with judge.py.

Also runs a paired Wilcoxon signed-rank test (System vs each baseline, per
dimension) since PLAN §6.5's exit criteria call for a documented
statistical comparison, and Wilcoxon (not a t-test) is appropriate here:
n=20 paired ordinal (1-5) judge ratings, not assumed normal.

Inter-rater reliability against the human survey (SOT §19.4) is computed
separately in human_eval_analysis.py once real survey data exists --
that comparison is blocked on human data collection (PLAN §6.3), not on
anything this script does.
"""

import asyncio
import json
import statistics
from pathlib import Path

from scipy import stats

from system.agents import analyzer, critic, generator
from system.evaluation.baselines import baseline_a_descriptive, baseline_b_zero_shot
from system.evaluation.eval_video_inputs import EVAL_VIDEO_INPUTS
from system.evaluation.judge import judge_title

OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DIMENSIONS = ["curiosity", "urgency", "relevance", "overall"]
CONDITIONS = ["baseline_a", "baseline_b", "system"]


async def run_one(video_input):
    brief = await analyzer.run(video_input)
    gen_out = await generator.run(brief, video_input.video_category)
    critic_out = await critic.run(brief, gen_out, video_input.video_category)
    system_title = critic_out.top_title or (
        gen_out.candidates[0].title if gen_out.candidates else ""
    )

    baseline_a_title = baseline_a_descriptive(video_input)
    baseline_b_title = await baseline_b_zero_shot(video_input)

    titles = {"baseline_a": baseline_a_title, "baseline_b": baseline_b_title, "system": system_title}

    scores = {}
    for name, title in titles.items():
        score = await judge_title(brief.core_promise, title)
        scores[name] = score.model_dump()

    return {
        "video_category": video_input.video_category,
        "core_promise": brief.core_promise,
        "titles": titles,
        "scores": scores,
    }


def _paired_test(system_scores, baseline_scores):
    """Wilcoxon signed-rank test; returns None if all differences are zero
    (scipy raises in that degenerate case rather than returning a p-value).
    """
    diffs = [s - b for s, b in zip(system_scores, baseline_scores)]
    if all(d == 0 for d in diffs):
        return {"statistic": None, "p_value": None, "note": "no difference between conditions"}
    result = stats.wilcoxon(system_scores, baseline_scores)
    return {"statistic": float(result.statistic), "p_value": float(result.pvalue)}


async def main():
    print(f"Running {len(EVAL_VIDEO_INPUTS)} videos x 3 conditions = "
          f"{len(EVAL_VIDEO_INPUTS) * 3} judge evaluations...")

    per_video = []
    for i, video_input in enumerate(EVAL_VIDEO_INPUTS, 1):
        result = await run_one(video_input)
        per_video.append(result)
        print(f"[{i}/{len(EVAL_VIDEO_INPUTS)}] {video_input.video_category}")

    means = {
        condition: {
            dim: statistics.mean(r["scores"][condition][dim] for r in per_video)
            for dim in DIMENSIONS
        }
        for condition in CONDITIONS
    }

    significance = {}
    for baseline in ("baseline_a", "baseline_b"):
        significance[f"system_vs_{baseline}"] = {
            dim: _paired_test(
                [r["scores"]["system"][dim] for r in per_video],
                [r["scores"][baseline][dim] for r in per_video],
            )
            for dim in DIMENSIONS
        }

    summary = {"n_videos": len(per_video), "mean_scores_by_condition": means, "significance": significance}
    print("\n=== Mean scores by condition ===")
    print(json.dumps(means, indent=2))
    print("\n=== Significance (Wilcoxon signed-rank, System vs baseline) ===")
    print(json.dumps(significance, indent=2))

    with open(OUT_DIR / "llm_judge_results.json", "w") as f:
        json.dump({"summary": summary, "per_video": per_video}, f, indent=2)

    print(f"\nSaved -> {OUT_DIR / 'llm_judge_results.json'}")


if __name__ == "__main__":
    asyncio.run(main())
