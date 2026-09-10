"""pCTR scoring for the Critic Agent (SOT §16.4, §12.3; PLAN §4.1).

Loads the Sprint 1 model bundle once and exposes score_title(), which
applies the exact same feature pipeline used at training time
(system/pipeline/features.py) so live predictions aren't silently skewed
by a diverging transform.
"""

from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd

from system.pipeline.features import build_features_single

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "pctr_model.pkl"

_bundle = joblib.load(MODEL_PATH)
_model = _bundle["model"]
_feature_cols = _bundle["feature_cols"]
_encoders = _bundle["categorical_encoders"]

MODEL_NAME = _bundle["model_name"]


def _safe_encode(encoder, value) -> int:
    """Falls back to the encoder's first class for a value never seen in
    training (e.g. a POS tag from an empty title) rather than raising.
    """
    if value in encoder.classes_:
        return int(encoder.transform([value])[0])
    return 0


def score_title(title: str, category_id: int) -> Tuple[float, float]:
    """Returns (pctr_score, vader_compound) for a single title."""
    row = build_features_single(title, category_id).iloc[0]

    features = {}
    for col in _feature_cols:
        if col.endswith("_enc"):
            base_col = col[: -len("_enc")]
            features[col] = _safe_encode(_encoders[base_col], row[base_col])
        else:
            features[col] = row[col]

    X = pd.DataFrame([features])[_feature_cols].astype(float)
    pctr_score = float(_model.predict_proba(X)[0, 1])
    return pctr_score, float(row["vader_compound"])
