"""Builds the blinded stimulus set for the human evaluation survey
(SOT §19.3; PLAN §6.3).

*** This does not collect any human responses. It only prepares the
materials. Actually running the survey with n=50+ real participants is a
manual step for the researcher -- it cannot be automated or simulated,
and no response data should ever be fabricated for a thesis. ***

Reads system/evaluation/outputs/llm_judge_results.json (produced by
llm_judge_eval.py, which already generated all 3 conditions -- Baseline A,
Baseline B, System -- for 20 videos) and selects 10 of them per SOT §19.3,
then writes:

  - human_eval_stimulus.csv: participant-facing sheet. Each video appears
    once with its 3 titles under blinded labels ("Title 1/2/3"), with the
    condition-to-label mapping *independently shuffled per video* so
    participants can't learn a fixed pattern (e.g. "Title 3 is always the
    system"). Ratable on the 4-dimension rubric (Curiosity, Emotional
    Impact, Clarity, Trustworthiness, 1-5) from SOT §19.3.
  - human_eval_answer_key.csv: NOT for participants. Maps
    (video_id, blinded_label) -> real condition, for scoring after
    responses come in. Keep this separate from whatever survey tool
    (Google Forms, Typeform, etc.) is used to distribute the stimulus.
"""

import csv
import json
import random
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "outputs"
N_STIMULUS_VIDEOS = 10
CONDITIONS = ["baseline_a", "baseline_b", "system"]
RUBRIC_DIMENSIONS = ["curiosity", "emotional_impact", "clarity", "trustworthiness"]

random.seed(42)  # reproducible blinding order, not a secret


def main():
    with open(OUT_DIR / "llm_judge_results.json") as f:
        per_video = json.load(f)["per_video"]

    if len(per_video) < N_STIMULUS_VIDEOS:
        raise ValueError(
            f"Need at least {N_STIMULUS_VIDEOS} videos, found {len(per_video)}. "
            "Run llm_judge_eval.py first."
        )

    selected = per_video[:N_STIMULUS_VIDEOS]

    stimulus_rows = []
    answer_key_rows = []

    for video_id, run in enumerate(selected, 1):
        conditions = list(CONDITIONS)
        random.shuffle(conditions)  # independent blinding order per video

        row = {
            "video_id": video_id,
            "video_category": run["video_category"],
            "video_context": run["core_promise"],
        }
        for position, condition in enumerate(conditions, 1):
            label = f"title_{position}"
            row[label] = run["titles"][condition]
            for dim in RUBRIC_DIMENSIONS:
                row[f"{label}_{dim}_rating"] = ""  # blank for participants to fill in
            answer_key_rows.append(
                {"video_id": video_id, "blinded_label": label, "condition": condition}
            )
        stimulus_rows.append(row)

    stimulus_fields = (
        ["video_id", "video_category", "video_context"]
        + [
            f
            for pos in range(1, 4)
            for f in (
                [f"title_{pos}"] + [f"title_{pos}_{dim}_rating" for dim in RUBRIC_DIMENSIONS]
            )
        ]
    )
    with open(OUT_DIR / "human_eval_stimulus.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=stimulus_fields)
        writer.writeheader()
        writer.writerows(stimulus_rows)

    with open(OUT_DIR / "human_eval_answer_key.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["video_id", "blinded_label", "condition"])
        writer.writeheader()
        writer.writerows(answer_key_rows)

    print(f"Saved {len(stimulus_rows)}-video stimulus -> {OUT_DIR / 'human_eval_stimulus.csv'}")
    print(f"Saved answer key (keep private from participants) -> "
          f"{OUT_DIR / 'human_eval_answer_key.csv'}")
    print(
        "\nNext step (manual, not automatable): load human_eval_stimulus.csv into a "
        "survey tool (Google Forms / Typeform / etc.), have the 1-5 rating columns "
        "answered by n=50+ real participants (creators, marketing students, general "
        "users per SOT §19.3), export responses, then run human_eval_analysis.py "
        "against the exported CSV + the answer key."
    )


if __name__ == "__main__":
    main()
