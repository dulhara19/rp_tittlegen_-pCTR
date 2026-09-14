"""Bar chart of system-level eval metrics vs their SOT §19.1 targets, for
Chapter 6 (PLAN §6.5 requires "system metric bar chart" as one of the 3+
required charts). Run after system_eval.py.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent / "outputs"

with open(OUT_DIR / "system_eval_results.json") as f:
    data = json.load(f)["aggregate"]

# (label, measured value, target value, whether higher-is-better)
rows = [
    ("Acceptance Rate", data["acceptance_rate"], 0.60, True),
    ("Avg Top pCTR", data["avg_top_pctr"], 0.06, True),
    ("Avg VADER Arousal", data["avg_vader_arousal"], 0.40, True),
    ("Avg BERTScore", data["avg_bert_similarity"], 0.60, False),  # upper bound shown
    ("Avg Self-BLEU", data["avg_self_bleu"], 0.40, False),
    ("Latency P95 (s / 10)", data["latency_p95_seconds"] / 10, 1.0, False),
]

labels = [r[0] for r in rows]
measured = [r[1] for r in rows]
targets = [r[2] for r in rows]
colors = ["#2a9d8f" if data["targets_met"].get(k, True) else "#e76f51"
          for k in ["acceptance_rate", "avg_top_pctr", "avg_vader_arousal",
                     "avg_bert_similarity", "avg_self_bleu", "latency_p95_seconds"]]

x = range(len(labels))
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(x, measured, width=0.5, color=colors, label="Measured")
ax.scatter(x, targets, color="black", marker="_", s=400, linewidths=2, zorder=3, label="Target")
ax.set_xticks(list(x))
ax.set_xticklabels(labels, rotation=20, ha="right")
ax.set_title("System-Level Evaluation — Measured vs Target (SOT §19.1)")
ax.legend()
fig.tight_layout()
fig.savefig(OUT_DIR / "system_eval_bar_chart.png")
print(f"Saved -> {OUT_DIR / 'system_eval_bar_chart.png'}")
