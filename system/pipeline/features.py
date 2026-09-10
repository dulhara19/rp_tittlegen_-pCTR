"""pCTR feature pipeline — extracted from data_exploration.ipynb.

Kept as a single importable module (not duplicated in the notebook) so that
offline training (Sprint 1) and live scoring (Critic agent, Sprint 4) apply
the exact same transform to a title. Any divergence here would silently
skew pCTR predictions away from what pctr_model.pkl was trained on.
"""

import re

import emoji
import nltk
import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:  # fresh machine: pip doesn't ship NLTK data
    nltk.download("vader_lexicon", quiet=True)

vader = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")

NUMBER_RE = re.compile(r"\d+")
SUB_TIER_BINS = [0, 10_000, 100_000, 1_000_000, float("inf")]
SUB_TIER_LABELS = ["0-10K", "10K-100K", "100K-1M", "1M+"]


def number_value(title):
    m = NUMBER_RE.search(title.replace(",", ""))
    return float(m.group()) if m else 0.0


def first_word_type(title):
    words = title.split()
    if not words:
        return "UNKNOWN"
    doc = nlp(words[0])
    return doc[0].pos_ if len(doc) else "UNKNOWN"


def all_caps_ratio(title):
    words = [w for w in re.findall(r"[A-Za-z]+", title) if len(w) > 1]
    if not words:
        return 0.0
    return sum(1 for w in words if w.isupper()) / len(words)


def build_features(df, title_col="title", subscriber_col="subscriber_count"):
    out = df.copy()
    out["title_length_chars"] = out[title_col].str.len()
    out["title_word_count"] = out[title_col].str.split().apply(len)
    out["has_number"] = out[title_col].apply(lambda t: bool(NUMBER_RE.search(t)))
    out["number_value"] = out[title_col].apply(number_value)

    vs = out[title_col].apply(lambda t: vader.polarity_scores(t))
    out["vader_compound"] = vs.apply(lambda d: d["compound"])
    out["vader_positive"] = vs.apply(lambda d: d["pos"])

    out["first_word_type"] = out[title_col].apply(first_word_type)
    out["has_question"] = out[title_col].str.contains("\\?")
    out["has_exclamation"] = out[title_col].str.contains("!")
    out["all_caps_ratio"] = out[title_col].apply(all_caps_ratio)
    out["has_emoji"] = out[title_col].apply(lambda t: any(c in emoji.EMOJI_DATA for c in t))

    if subscriber_col in out.columns:
        out["channel_subscriber_tier"] = pd.cut(
            out[subscriber_col], bins=SUB_TIER_BINS, labels=SUB_TIER_LABELS, right=False
        ).astype(str)
    else:
        out["channel_subscriber_tier"] = SUB_TIER_LABELS[0]
    return out


def build_features_single(title: str, category_id: int, subscriber_count: int | None = None) -> pd.DataFrame:
    """Single-title convenience wrapper for live scoring (Critic agent)."""
    row = {"title": title, "category_id": category_id}
    if subscriber_count is not None:
        row["subscriber_count"] = subscriber_count
    df = pd.DataFrame([row])
    return build_features(df)
