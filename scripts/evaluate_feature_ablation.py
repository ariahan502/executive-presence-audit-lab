from __future__ import annotations

import csv
import math
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


NUMERIC_FEATURES = [
    "total_events",
    "page_views",
    "article_views",
    "cta_clicks",
    "newsletter_form_starts",
    "newsletter_submits",
    "consultation_form_starts",
    "path_step_count",
    "used_article_content",
    "clicked_cta",
    "started_high_intent_form",
]

BASE_CATEGORICAL = [
    "landing_page",
    "first_utm_source",
    "first_utm_medium",
]

MANUAL_TAXONOMY = [
    "first_content_theme",
    "first_message_framing",
    "audience_segment",
    "cta_style",
]

TEXT_DERIVED = [
    "text_derived_message_framing",
    "text_derived_audience_segment",
    "text_derived_cta_style",
]

MODEL_ASSISTED = [
    "model_assisted_message_framing",
    "model_assisted_audience_segment",
    "model_assisted_cta_style",
]


@dataclass
class FeatureSetResult:
    feature_set: str
    roc_auc: float
    pr_auc: float
    brier_score: float
    top_decile_capture: float
    precision_at_top_decile: float
    lead_score_capture_share: float
    validation_sessions: int
    validation_positives: int


def fetch_rows():
    create_app()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute(
            """
            with lead_quality as (
                select
                    session_id,
                    traffic_type,
                    avg(lead_score) as avg_lead_score
                from lead_scoring
                group by session_id, traffic_type
            )
            select
                lif.*,
                cmp.text_derived_message_framing,
                cmp.text_derived_audience_segment,
                cmp.text_derived_cta_style,
                cmp.model_assisted_message_framing,
                cmp.model_assisted_audience_segment,
                cmp.model_assisted_cta_style,
                coalesce(lq.avg_lead_score, 0.0) as avg_lead_score
            from lead_intent_features lif
            left join content_label_comparison cmp
                on cmp.page_url = lif.landing_page
            left join lead_quality lq
                on lq.session_id = lif.session_id
               and lq.traffic_type = lif.traffic_type
            where lif.traffic_type = 'synthetic'
            order by lif.session_id
            """
        ).fetchall()
    finally:
        conn.close()


def build_examples(rows, categorical_features: list[str]):
    examples = []
    labels = []
    lead_scores = []
    for row in rows:
        example = {}
        for feature in NUMERIC_FEATURES:
            example[feature] = row[feature]
        for feature in categorical_features:
            example[feature] = row[feature]
        examples.append(example)
        labels.append(int(row["target_consultation_lead"]))
        lead_scores.append(float(row["avg_lead_score"] or 0.0))
    return examples, labels, lead_scores


def evaluate_feature_set(rows, feature_set_name: str, categorical_features: list[str], train_indices, validation_indices) -> FeatureSetResult:
    examples, labels, lead_scores = build_examples(rows, categorical_features)

    train_examples = [examples[index] for index in train_indices]
    train_labels = [labels[index] for index in train_indices]
    validation_examples = [examples[index] for index in validation_indices]
    validation_labels = [labels[index] for index in validation_indices]
    validation_lead_scores = [lead_scores[index] for index in validation_indices]

    model = Pipeline(
        steps=[
            ("vectorizer", DictVectorizer(sparse=False)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    model.fit(train_examples, train_labels)
    probabilities = model.predict_proba(validation_examples)[:, 1]

    roc_auc = roc_auc_score(validation_labels, probabilities)
    pr_auc = average_precision_score(validation_labels, probabilities)
    brier = brier_score_loss(validation_labels, probabilities)

    ranked = sorted(
        zip(probabilities, validation_labels, validation_lead_scores),
        key=lambda item: item[0],
        reverse=True,
    )
    top_k = max(1, math.ceil(len(ranked) * 0.1))
    top_ranked = ranked[:top_k]
    positives = sum(validation_labels)
    captured_positives = sum(label for _, label, _ in top_ranked)
    top_decile_capture = captured_positives / positives if positives else 0.0
    precision_at_top_decile = captured_positives / top_k if top_k else 0.0

    total_lead_score = sum(score for label, score in zip(validation_labels, validation_lead_scores) if label == 1)
    captured_lead_score = sum(score for _, label, score in top_ranked if label == 1)
    lead_score_capture_share = captured_lead_score / total_lead_score if total_lead_score else 0.0

    return FeatureSetResult(
        feature_set=feature_set_name,
        roc_auc=roc_auc,
        pr_auc=pr_auc,
        brier_score=brier,
        top_decile_capture=top_decile_capture,
        precision_at_top_decile=precision_at_top_decile,
        lead_score_capture_share=lead_score_capture_share,
        validation_sessions=len(validation_labels),
        validation_positives=positives,
    )


def write_results(results: list[FeatureSetResult]):
    output_path = BASE_DIR / "analytics" / "feature_ablation_results.csv"
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "feature_set",
                "roc_auc",
                "pr_auc",
                "brier_score",
                "top_decile_capture",
                "precision_at_top_decile",
                "lead_score_capture_share",
                "validation_sessions",
                "validation_positives",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "feature_set": result.feature_set,
                    "roc_auc": round(result.roc_auc, 6),
                    "pr_auc": round(result.pr_auc, 6),
                    "brier_score": round(result.brier_score, 6),
                    "top_decile_capture": round(result.top_decile_capture, 6),
                    "precision_at_top_decile": round(result.precision_at_top_decile, 6),
                    "lead_score_capture_share": round(result.lead_score_capture_share, 6),
                    "validation_sessions": result.validation_sessions,
                    "validation_positives": result.validation_positives,
                }
            )
    return output_path


def main():
    rows = fetch_rows()
    if len(rows) < 20:
        raise SystemExit("Need at least 20 synthetic sessions to run feature ablation evaluation.")

    labels = [int(row["target_consultation_lead"]) for row in rows]
    if len(set(labels)) < 2:
        raise SystemExit("Need both positive and negative examples to run feature ablation evaluation.")

    indices = list(range(len(rows)))
    train_indices, validation_indices = train_test_split(
        indices,
        test_size=0.3,
        random_state=42,
        stratify=labels,
    )

    feature_sets = [
        ("behavior_source_path", BASE_CATEGORICAL),
        ("manual_taxonomy", BASE_CATEGORICAL + MANUAL_TAXONOMY),
        ("text_derived_taxonomy", BASE_CATEGORICAL + ["first_content_theme"] + TEXT_DERIVED),
        ("model_assisted_taxonomy", BASE_CATEGORICAL + ["first_content_theme"] + MODEL_ASSISTED),
    ]

    results = [
        evaluate_feature_set(rows, feature_set_name, categorical_features, train_indices, validation_indices)
        for feature_set_name, categorical_features in feature_sets
    ]
    output_path = write_results(results)

    print(f"Evaluated {len(results)} feature sets on {len(rows)} synthetic sessions.")
    for result in results:
        print(
            f"{result.feature_set}: "
            f"ROC AUC={result.roc_auc:.4f}, "
            f"PR AUC={result.pr_auc:.4f}, "
            f"Brier={result.brier_score:.4f}, "
            f"Top-decile capture={result.top_decile_capture:.4f}, "
            f"Precision@top-decile={result.precision_at_top_decile:.4f}, "
            f"Lead-score capture={result.lead_score_capture_share:.4f}"
        )
    print(f"Results written to {output_path}.")


if __name__ == "__main__":
    main()
