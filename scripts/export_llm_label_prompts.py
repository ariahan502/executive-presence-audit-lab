from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH


SYSTEM_PROMPT = (
    "You are labeling growth-analytics content assets for message framing, audience segment, "
    "and CTA style. Use the provided schema only. Prefer business interpretation over surface wording."
)

USER_INSTRUCTION = """Classify the content asset into:
1. message_framing: one of [authority, practical, industry_specific, conversion]
2. audience_segment: one of [cross_audience, women_in_finance, client_facing_leaders, promotion_readiness]
3. cta_style: one of [direct_conversion, bridge_to_conversion, nurture_capture, high_intent_form]
4. notes: one short sentence on why these labels make sense for conversion analysis

Return strict JSON with keys:
message_framing, audience_segment, cta_style, notes
"""


def fetch_assets():
    create_app()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute(
            """
            select
                asset_id,
                asset_type,
                page_url,
                title,
                body_summary,
                content_theme,
                message_framing,
                audience_segment,
                primary_cta,
                cta_style
            from content_assets
            order by asset_id
            """
        ).fetchall()
    finally:
        conn.close()


def main():
    rows = fetch_assets()
    output_path = BASE_DIR / "analytics" / "content_label_prompts.jsonl"
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            payload = {
                "asset_id": row["asset_id"],
                "system": SYSTEM_PROMPT,
                "user": {
                    "instruction": USER_INSTRUCTION,
                    "asset": {
                        "asset_type": row["asset_type"],
                        "page_url": row["page_url"],
                        "title": row["title"],
                        "body_summary": row["body_summary"],
                        "content_theme": row["content_theme"],
                        "primary_cta": row["primary_cta"],
                        "manual_labels": {
                            "message_framing": row["message_framing"],
                            "audience_segment": row["audience_segment"],
                            "cta_style": row["cta_style"],
                        },
                    },
                },
            }
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")

    print(f"Exported {len(rows)} LLM-ready content labeling prompts to {output_path}.")


if __name__ == "__main__":
    main()
