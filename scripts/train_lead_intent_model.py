from pathlib import Path
import csv
import sqlite3
import sys
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


FEATURE_COLUMNS = [
    "landing_page",
    "first_content_theme",
    "first_message_framing",
    "first_utm_source",
    "first_utm_medium",
    "audience_segment",
    "cta_style",
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

def fetch_rows():
    create_app()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute(
            """
            select *
            from lead_intent_features
            where traffic_type = 'synthetic'
            order by session_id
            """
        ).fetchall()
    finally:
        conn.close()


def build_examples(rows):
    examples = []
    labels = []
    for row in rows:
        examples.append({column: row[column] for column in FEATURE_COLUMNS})
        labels.append(int(row["target_consultation_lead"]))
    return examples, labels


@dataclass
class SplitPrediction:
    row: sqlite3.Row
    split: str
    probability: float


def write_predictions(predictions):
    output_path = BASE_DIR / "analytics" / "lead_intent_predictions.csv"
    fieldnames = [
        "session_id",
        "traffic_type",
        "dataset_split",
        "landing_page",
        "target_consultation_lead",
        "predicted_consultation_probability",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for prediction in predictions:
            row = prediction.row
            writer.writerow(
                {
                    "session_id": row["session_id"],
                    "traffic_type": row["traffic_type"],
                    "dataset_split": prediction.split,
                    "landing_page": row["landing_page"],
                    "target_consultation_lead": row["target_consultation_lead"],
                    "predicted_consultation_probability": round(float(prediction.probability), 6),
                }
            )
    return output_path


def main():
    rows = fetch_rows()
    if len(rows) < 8:
        raise SystemExit("Need at least 8 synthetic sessions in lead_intent_features to train the baseline model.")

    examples, labels = build_examples(rows)
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        raise SystemExit("Need both positive and negative examples to train the baseline model.")

    indices = list(range(len(rows)))
    train_indices, validation_indices = train_test_split(
        indices,
        test_size=0.3,
        random_state=42,
        stratify=labels,
    )

    train_examples = [examples[index] for index in train_indices]
    train_labels = [labels[index] for index in train_indices]
    validation_examples = [examples[index] for index in validation_indices]
    validation_labels = [labels[index] for index in validation_indices]

    model = Pipeline(
        steps=[
            ("vectorizer", DictVectorizer(sparse=False)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    model.fit(train_examples, train_labels)

    validation_probabilities = model.predict_proba(validation_examples)[:, 1]
    roc_auc = roc_auc_score(validation_labels, validation_probabilities)
    pr_auc = average_precision_score(validation_labels, validation_probabilities)

    train_probabilities = model.predict_proba(train_examples)[:, 1]
    predictions = []
    for index, probability in zip(train_indices, train_probabilities):
        predictions.append(SplitPrediction(row=rows[index], split="train", probability=float(probability)))
    for index, probability in zip(validation_indices, validation_probabilities):
        predictions.append(SplitPrediction(row=rows[index], split="validation", probability=float(probability)))
    predictions.sort(key=lambda item: item.row["session_id"])

    output_path = write_predictions(predictions)

    print(f"Trained baseline lead-intent model on {len(labels)} synthetic sessions.")
    print(f"Train sessions: {len(train_labels)}")
    print(f"Validation sessions: {len(validation_labels)}")
    print(f"Positive sessions: {positives}")
    print(f"Negative sessions: {negatives}")
    print(f"Validation ROC AUC: {roc_auc:.4f}")
    print(f"Validation PR AUC: {pr_auc:.4f}")
    print(f"Predictions written to {output_path}.")


if __name__ == "__main__":
    main()
