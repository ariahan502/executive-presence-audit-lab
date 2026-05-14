from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH


INPUT_PATH = BASE_DIR / "analytics" / "content_label_model_assisted.jsonl"


def main():
    create_app()
    if not INPUT_PATH.exists():
        raise SystemExit(f"Missing {INPUT_PATH}.")

    rows = []
    with INPUT_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    conn = sqlite3.connect(DATABASE_PATH)
    try:
        conn.execute("delete from content_label_model_assisted")
        for row in rows:
            conn.execute(
                """
                insert into content_label_model_assisted (
                    asset_id,
                    model_provider,
                    model_name,
                    prompt_version,
                    message_framing,
                    audience_segment,
                    cta_style,
                    notes,
                    label_source,
                    updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, 'interactive_model_assisted', current_timestamp)
                """,
                (
                    row["asset_id"],
                    row["model_provider"],
                    row["model_name"],
                    row["prompt_version"],
                    row["message_framing"],
                    row["audience_segment"],
                    row["cta_style"],
                    row.get("notes", ""),
                ),
            )
        conn.commit()
    finally:
        conn.close()

    print(f"Imported {len(rows)} model-assisted labels into {DATABASE_PATH}.")


if __name__ == "__main__":
    main()
