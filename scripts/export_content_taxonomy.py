from pathlib import Path
import csv
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH


def main():
    create_app()
    output_path = BASE_DIR / "analytics" / "content_taxonomy_snapshot.csv"
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            select
                asset_id,
                asset_type,
                page_url,
                title,
                content_theme,
                message_framing,
                funnel_stage_intent,
                audience_segment,
                primary_cta,
                cta_style,
                taxonomy_version,
                label_source
            from content_assets
            order by asset_type, page_url
            """
        ).fetchall()
    finally:
        conn.close()

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else [])
        if rows:
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))

    print(f"Exported {len(rows)} content taxonomy rows to {output_path}.")


if __name__ == "__main__":
    main()
