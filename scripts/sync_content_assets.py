from pathlib import Path
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH
from app.content_registry import CONTENT_ASSETS


def main():
    create_app()
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        conn.executemany(
            """
            insert into content_assets (
                asset_id, asset_type, page_url, title, content_theme,
                message_framing, funnel_stage_intent, audience_segment,
                primary_cta, cta_style, body_summary, slug,
                taxonomy_version, label_source
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            on conflict(asset_id) do update set
                asset_type = excluded.asset_type,
                page_url = excluded.page_url,
                title = excluded.title,
                content_theme = excluded.content_theme,
                message_framing = excluded.message_framing,
                funnel_stage_intent = excluded.funnel_stage_intent,
                audience_segment = excluded.audience_segment,
                primary_cta = excluded.primary_cta,
                cta_style = excluded.cta_style,
                body_summary = excluded.body_summary,
                slug = excluded.slug,
                taxonomy_version = excluded.taxonomy_version,
                label_source = excluded.label_source
            """,
            [
                (
                    asset.asset_id,
                    asset.asset_type,
                    asset.page_url,
                    asset.title,
                    asset.content_theme,
                    asset.message_framing,
                    asset.funnel_stage_intent,
                    asset.audience_segment,
                    asset.primary_cta,
                    asset.cta_style,
                    asset.body_summary,
                    asset.slug,
                    "v1_manual",
                    "manual",
                )
                for asset in CONTENT_ASSETS
            ],
        )
        conn.commit()
        print(f"Synchronized {len(CONTENT_ASSETS)} content assets into {DATABASE_PATH}.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
