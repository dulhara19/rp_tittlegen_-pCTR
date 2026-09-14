"""System-level evaluation (SOT §19.1; PLAN §6.2).

Runs 20 diverse video transcripts (system/evaluation/eval_video_inputs.py)
through the full Analyzer -> Generator -> Critic pipeline via the same
LangGraph entrypoint the API uses (system/pipeline/graph.run_pipeline), and
records the metrics SOT §19.1 defines against their stated targets:

  Title Acceptance Rate  (% candidates passing NLI)        > 60%
  pCTR Score (avg)       (avg pCTR of top-ranked titles)   > 6%   (0.06)
  VADER Arousal (avg)    (avg |compound| across candidates) > 0.4
  BERTScore (avg)        (avg title-vs-summary similarity) 0.35-0.60
  Self-BLEU (diversity)  (overlap within a batch)          < 0.4
  Latency (P95)          (end-to-end pipeline time)        < 10s

Makes real LLM + local-model calls for all 20 cases -- this is the
authoritative Sprint 6 run, not a subset like earlier sprints used for
speed, since these are the actual numbers going into Chapter 6.
"""

import asyncio
import json
import statistics
import time
from pathlib import Path

from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu

from system.evaluation.eval_video_inputs import EVAL_VIDEO_INPUTS
from system.pipeline.graph import run_pipeline

OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

_SMOOTHING = SmoothingFunction().method1

TARGETS = {
    "acceptance_rate": (">", 0.60),
    "avg_top_pctr": (">", 0.06),
    "avg_vader_arousal": (">", 0.4),
    "avg_bert_similarity": ("range", (0.35, 0.60)),
    "avg_self_bleu": ("<", 0.4),
    "latency_p95_seconds": ("<", 10.0),
}


def self_bleu(titles: list[str]) -> float:
    """Mean BLEU of each title against the rest of the batch as references.
    Lower = more diverse (SOT §19.1).
    """
    tokenized = [t.split() for t in titles]
    scores = []
    for i, hyp in enumerate(tokenized):
        refs = [tok for j, tok in enumerate(tokenized) if j != i]
        if not refs or not hyp:
            continue
        scores.append(sentence_bleu(refs, hyp, smoothing_function=_SMOOTHING))
    return sum(scores) / len(scores) if scores else 0.0


async def run_one(video_input):
    start = time.perf_counter()
    result = await run_pipeline(video_input)
    elapsed = time.perf_counter() - start

    if result.get("error"):
        return {
            "video_category": video_input.video_category,
            "error": result["error"],
            "elapsed": elapsed,
        }

    critic_output = result["critic_output"]
    candidates = critic_output.scored_candidates

    top = next((c for c in candidates if c.title == critic_output.top_title), None)

    return {
        "video_category": video_input.video_category,
        "elapsed": elapsed,
        "n_candidates": len(candidates),
        "n_valid": sum(1 for c in candidates if c.is_valid),
        "top_pctr": top.pctr_score if top else None,
        "vader_arousals": [abs(c.vader_compound) for c in candidates],
        "bert_similarities": [c.bert_similarity for c in candidates],
        "self_bleu": self_bleu([c.title for c in candidates]),
        "top_title": critic_output.top_title,
        "rejection_log": critic_output.rejection_log,
    }


def _check_target(name, value):
    kind, target = TARGETS[name]
    if kind == ">":
        return value > target
    if kind == "<":
        return value < target
    if kind == "range":
        lo, hi = target
        return lo <= value <= hi
    raise ValueError(kind)


async def main():
    print(f"Running {len(EVAL_VIDEO_INPUTS)} video inputs through the full pipeline...")
    per_run = []
    for i, video_input in enumerate(EVAL_VIDEO_INPUTS, 1):
        result = await run_one(video_input)
        per_run.append(result)
        status = "ERROR" if "error" in result else f"{result['elapsed']:.1f}s"
        print(f"[{i}/{len(EVAL_VIDEO_INPUTS)}] {video_input.video_category:25s} {status}")

    ok_runs = [r for r in per_run if "error" not in r]
    errored = [r for r in per_run if "error" in r]

    total_candidates = sum(r["n_candidates"] for r in ok_runs)
    total_valid = sum(r["n_valid"] for r in ok_runs)
    all_vader = [v for r in ok_runs for v in r["vader_arousals"]]
    all_bert = [b for r in ok_runs for b in r["bert_similarities"]]
    top_pctrs = [r["top_pctr"] for r in ok_runs if r["top_pctr"] is not None]
    self_bleus = [r["self_bleu"] for r in ok_runs]
    latencies = sorted(r["elapsed"] for r in per_run)

    def percentile(data, p):
        if not data:
            return None
        k = (len(data) - 1) * p
        f, c = int(k), min(int(k) + 1, len(data) - 1)
        return data[f] if f == c else data[f] + (data[c] - data[f]) * (k - f)

    aggregate = {
        "n_runs": len(per_run),
        "n_errors": len(errored),
        "acceptance_rate": total_valid / total_candidates if total_candidates else 0.0,
        "avg_top_pctr": statistics.mean(top_pctrs) if top_pctrs else None,
        "avg_vader_arousal": statistics.mean(all_vader) if all_vader else None,
        "avg_bert_similarity": statistics.mean(all_bert) if all_bert else None,
        "avg_self_bleu": statistics.mean(self_bleus) if self_bleus else None,
        "latency_p50_seconds": percentile(latencies, 0.50),
        "latency_p95_seconds": percentile(latencies, 0.95),
    }
    aggregate["targets_met"] = {
        name: _check_target(name, aggregate[name])
        for name in TARGETS
        if aggregate.get(name) is not None
    }

    print("\n=== Aggregate results ===")
    print(json.dumps(aggregate, indent=2))

    with open(OUT_DIR / "system_eval_results.json", "w") as f:
        json.dump({"aggregate": aggregate, "per_run": per_run}, f, indent=2)

    print(f"\nSaved -> {OUT_DIR / 'system_eval_results.json'}")


if __name__ == "__main__":
    asyncio.run(main())
