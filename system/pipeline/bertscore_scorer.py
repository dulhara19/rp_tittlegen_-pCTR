"""BERTScore relevance check for the Critic Agent (SOT §14.5, §17.4; PLAN §4.3).

bert_similarity < 0.30 -> flag as potentially off-topic (Critic's job, not
this module's — this just returns the raw score).
bert_similarity > 0.60 -> potentially boring/descriptive but acceptable.

Loads the scoring model (roberta-large, bert-score's default for English)
eagerly at module import via a persistent BERTScorer instance, not lazily
on first use -- see nli_scorer.py's docstring for why: concurrently loading
this model on one thread while nli_scorer.py loads bart-large-mnli on
another corrupts transformers/accelerate's meta-device weight
materialization. Eager loading at import avoids racing that against
another model's load on the first real request.
"""

import threading

from bert_score import BERTScorer

_scorer = BERTScorer(lang="en")
_lock = threading.Lock()


def bert_similarity(title: str, core_promise: str) -> float:
    with _lock:
        _, _, f1 = _scorer.score([title], [core_promise])
    return float(f1[0])
