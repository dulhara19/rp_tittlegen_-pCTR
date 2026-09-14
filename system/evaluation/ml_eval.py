"""Offline ML evaluation of the pCTR model (SOT §19.2; PLAN §6.1).

Reconstructs the exact 70/15/15 train/val/test split used at training time
(same random_state=42, same stratify) so the held-out test set here is the
same rows model_training.ipynb never touched, then evaluates the already
trained model_bundle (system/models/pctr_model.pkl) against it.

Targets (SOT §19.2): F1 > 0.75, ROC-AUC > 0.80. Sprint 1 already found the
model falls short of these (val F1 ~0.696, test F1 ~0.690, deferred rather
than re-tuned — see PLAN_IMPLEMENTATION.md §1.6). This script doesn't
re-tune; it re-confirms those numbers with proper plots for Chapter 6
(Sprint 1 only produced a feature-importance plot, not ROC/confusion
matrix).
"""

import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "processed" / "labeled_titles.csv"
MODEL_PATH = BASE / "models" / "pctr_model.pkl"
OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLS = [
    "title_length_chars", "title_word_count", "has_number", "number_value",
    "vader_compound", "vader_positive", "has_question", "has_exclamation",
    "all_caps_ratio", "has_emoji", "category_id",
]
CATEGORICAL_COLS = ["first_word_type", "channel_subscriber_tier"]

F1_TARGET = 0.75
ROC_AUC_TARGET = 0.80


def _prepare_xy(df):
    df = df.copy()
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col + "_enc"] = le.fit_transform(df[col].astype(str))
    feature_cols = FEATURE_COLS + [c + "_enc" for c in CATEGORICAL_COLS]
    X = df[feature_cols].astype(float)
    y = df["label"].astype(int)
    return X, y, feature_cols


def main():
    df = pd.read_csv(DATA_PATH)
    X, y, feature_cols = _prepare_xy(df)

    # Same split as model_training.ipynb -- identical random_state/stratify
    # reproduces the exact same held-out test rows.
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )
    print(f"train={len(X_train)} val={len(X_val)} test={len(X_test)}")

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    model_feature_cols = bundle["feature_cols"]

    X_test_ordered = X_test[model_feature_cols]
    preds = model.predict(X_test_ordered)
    proba = model.predict_proba(X_test_ordered)[:, 1]

    metrics = {
        "model_name": bundle["model_name"],
        "f1": float(f1_score(y_test, preds)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "precision": float(precision_score(y_test, preds)),
        "recall": float(recall_score(y_test, preds)),
        "f1_target_met": bool(f1_score(y_test, preds) > F1_TARGET),
        "roc_auc_target_met": bool(roc_auc_score(y_test, proba) > ROC_AUC_TARGET),
    }
    print(json.dumps(metrics, indent=2))

    # ROC curve
    fig, ax = plt.subplots(figsize=(6, 6))
    RocCurveDisplay.from_predictions(y_test, proba, ax=ax, name=bundle["model_name"])
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Chance")
    ax.set_title("pCTR Model — ROC Curve (held-out test set)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "roc_curve.png")
    plt.close(fig)

    # Confusion matrix
    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay(cm, display_labels=["Below median (0)", "Above median (1)"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title("pCTR Model — Confusion Matrix (held-out test set)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "confusion_matrix.png")
    plt.close(fig)

    # Feature importance (re-generated here alongside the other two plots
    # for a single Chapter 6 output directory, rather than only living in
    # system/models/ from Sprint 1)
    importances = getattr(model, "feature_importances_", None)
    if importances is not None:
        order = np.argsort(importances)[::-1][:10]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh([model_feature_cols[i] for i in order][::-1], importances[order][::-1])
        ax.set_xlabel("Importance")
        ax.set_title(f"Top 10 Feature Importances ({bundle['model_name']})")
        fig.tight_layout()
        fig.savefig(OUT_DIR / "feature_importance.png")
        plt.close(fig)

    with open(OUT_DIR / "ml_eval_results.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved plots + results.json -> {OUT_DIR}")


if __name__ == "__main__":
    main()
