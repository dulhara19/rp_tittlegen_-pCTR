"""NLI faithfulness gate for the Critic Agent (SOT §14.5, §17.3; PLAN §4.4).

premise = generated title, hypothesis = core_promise from the VideoBrief.
"contradiction" means the title claims something the video brief doesn't
support — the Critic hard-rejects those.

Loads facebook/bart-large-mnli eagerly at module import, not lazily on
first use. The Critic fans scoring out across candidates concurrently
(asyncio.gather over asyncio.to_thread, see system/agents/critic.py), and a
lazy first load raced against bertscore_scorer.py's own lazy load of a
*different* model on a different thread -- both relying on
transformers/accelerate's meta-device weight materialization, which isn't
safe under that kind of cross-model concurrent loading. Per-module-load
locks didn't fix it (confirmed: a single isolated to_thread call succeeds,
but two different models loading concurrently on two threads still
corrupts state) -- eager loading at import sidesteps the problem entirely
by paying the ~1.6GB download/load cost once at process startup instead of
racing it against BERTScore's load on the first real request.
"""

import threading

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

_MODEL_NAME = "facebook/bart-large-mnli"
_tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
_model = AutoModelForSequenceClassification.from_pretrained(_MODEL_NAME)
_model.eval()

_lock = threading.Lock()


def classify_nli(premise: str, hypothesis: str) -> str:
    """Returns one of "entailment", "neutral", "contradiction"."""
    with _lock:
        inputs = _tokenizer(premise, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = _model(**inputs).logits
        label_id = int(torch.argmax(logits, dim=-1)[0])
        return _model.config.id2label[label_id].lower()
