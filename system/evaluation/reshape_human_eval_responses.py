"""Reshape the Google Forms export (SOT §19.3; PLAN §6.3) from wide to the
long format `human_eval_analysis.py` expects: participant_id, video_id,
blinded_label, dimension, rating.

The form asked about video_id 1, 3, 6 (in that order), each with title_1,
title_2, title_3 (in that order), each rated on 4 dimensions in this fixed
order: curiosity, emotional_impact, clarity, trustworthiness. That gives
3 videos x 3 titles x 4 dims = 36 rating columns after the 3 leading
metadata columns (timestamp, participant name, category).

Usage: python -m system.evaluation.reshape_human_eval_responses \
    "research/YouTube Title Preference Study .csv/YouTube Title Preference Study .csv" \
    system/evaluation/outputs/human_eval_responses_long.csv
"""

import csv
import sys

VIDEO_IDS = [1, 3, 6]
BLINDED_LABELS = ["title_1", "title_2", "title_3"]
DIMENSIONS = ["curiosity", "emotional_impact", "clarity", "trustworthiness"]

N_META_COLS = 3  # timestamp, name, category


def reshape(src_path, dst_path):
    with open(src_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    n_rating_cols = len(VIDEO_IDS) * len(BLINDED_LABELS) * len(DIMENSIONS)
    expected_cols = N_META_COLS + n_rating_cols
    if len(header) != expected_cols:
        raise ValueError(
            f"Expected {expected_cols} columns ({N_META_COLS} meta + {n_rating_cols} "
            f"rating), got {len(header)}. Check the form layout hasn't changed."
        )

    out_rows = []
    skipped = 0
    for row in rows:
        participant_id = row[1].strip()
        if not participant_id:
            continue
        col = N_META_COLS
        for video_id in VIDEO_IDS:
            for blinded_label in BLINDED_LABELS:
                for dimension in DIMENSIONS:
                    raw = row[col].strip()
                    col += 1
                    if not raw:
                        skipped += 1
                        continue
                    out_rows.append(
                        {
                            "participant_id": participant_id,
                            "video_id": video_id,
                            "blinded_label": blinded_label,
                            "dimension": dimension,
                            "rating": raw,
                        }
                    )

    with open(dst_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["participant_id", "video_id", "blinded_label", "dimension", "rating"]
        )
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"{len(rows)} respondents -> {len(out_rows)} long rows ({skipped} blank cells skipped)")
    print(f"Saved -> {dst_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m system.evaluation.reshape_human_eval_responses <src.csv> <dst.csv>")
        sys.exit(1)
    reshape(sys.argv[1], sys.argv[2])
