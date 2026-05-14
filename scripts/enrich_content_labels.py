from __future__ import annotations

import math
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, DATABASE_PATH

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TOKEN_REPLACEMENTS = {
    "/": " ",
    "-": " ",
    "_": " ",
    ",": " ",
    ".": " ",
    ":": " ",
    ";": " ",
}


FRAMING_PROTOTYPES = {
    "authority": "executive authority senior leadership visibility promotion signal strategic influence credibility",
    "practical": "practical how to trust client facing visible credibility communication execution applied advice",
    "industry_specific": "women in finance finance banking industry specific leadership environment visibility fit",
    "conversion": "consultation request audit direct assessment high intent conversion next step",
}

CTA_PROTOTYPES = {
    "direct_conversion": "request consultation get audit direct next step high commitment",
    "bridge_to_conversion": "learn more next step article to consultation bridge content path",
    "nurture_capture": "newsletter subscribe join updates lower commitment nurture",
    "high_intent_form": "submit request detailed form consultation high intent",
}

AUDIENCE_PROTOTYPES = {
    "women_in_finance": "women finance banking investment promotion visibility industry specific leadership",
    "client_facing_leaders": "client facing consultants advisors sellers trust presentation credibility external relationships",
    "promotion_readiness": "promotion executive presence senior stakeholders leadership signal career progression",
    "cross_audience": "general executive presence leadership credibility broad advisory audience",
}

KEYWORD_GROUPS = {
    "authority": {"executive", "authority", "leadership", "promotion", "signal", "signals", "readiness", "senior"},
    "practical": {"practical", "credibility", "client", "facing", "trust", "visible", "professionals", "how"},
    "industry_specific": {"women", "finance", "industry", "banking", "environment"},
    "conversion": {"consultation", "request", "audit", "conversion", "submit", "qualified"},
    "direct_conversion": {"request", "consultation", "audit", "direct", "submit"},
    "bridge_to_conversion": {"article", "next", "step", "bridge", "learn"},
    "nurture_capture": {"newsletter", "subscribe", "join", "updates", "nurture"},
    "high_intent_form": {"form", "request", "consultation", "submit", "detailed"},
    "women_in_finance": {"women", "finance", "banking"},
    "client_facing_leaders": {"client", "facing", "consultants", "advisors", "trust"},
    "promotion_readiness": {"promotion", "stakeholders", "visibility", "readiness"},
    "cross_audience": {"executive", "leadership", "credibility", "advisory"},
}


def normalize_text(text: str) -> str:
    value = text.lower()
    for source, target in TOKEN_REPLACEMENTS.items():
        value = value.replace(source, target)
    return " ".join(value.split())


def tokenize(text: str) -> list[str]:
    return normalize_text(text).split()


def keyword_score(tokens: Iterable[str], keyword_group: set[str]) -> float:
    counts = Counter(tokens)
    return float(sum(counts[token] for token in keyword_group))


def top_label(score_map: dict[str, float]) -> tuple[str, float]:
    ordered = sorted(score_map.items(), key=lambda item: item[1], reverse=True)
    best_label, best_score = ordered[0]
    second_score = ordered[1][1] if len(ordered) > 1 else 0.0
    confidence = round(best_score - second_score, 4)
    return best_label, confidence


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
                content_theme,
                message_framing,
                funnel_stage_intent,
                audience_segment,
                primary_cta,
                cta_style,
                body_summary
            from content_assets
            order by asset_id
            """
        ).fetchall()
    finally:
        conn.close()


def build_similarity_lookup(asset_texts: dict[str, str], prototypes: dict[str, str]) -> dict[str, dict[str, float]]:
    vectorizer = TfidfVectorizer()
    corpus_labels = list(asset_texts.keys()) + [f"prototype::{name}" for name in prototypes]
    corpus_texts = list(asset_texts.values()) + list(prototypes.values())
    matrix = vectorizer.fit_transform(corpus_texts)
    asset_matrix = matrix[: len(asset_texts)]
    prototype_matrix = matrix[len(asset_texts) :]
    similarity = cosine_similarity(asset_matrix, prototype_matrix)

    lookup: dict[str, dict[str, float]] = {}
    prototype_names = list(prototypes.keys())
    for row_index, asset_id in enumerate(asset_texts):
        lookup[asset_id] = {
            prototype_name: float(similarity[row_index][prototype_index])
            for prototype_index, prototype_name in enumerate(prototype_names)
        }
    return lookup


def main():
    rows = fetch_assets()
    if not rows:
        raise SystemExit("No content assets found. Run scripts/sync_content_assets.py first.")

    asset_texts = {
        row["asset_id"]: normalize_text(
            " ".join(
                [
                    row["title"] or "",
                    row["body_summary"] or "",
                    row["primary_cta"] or "",
                    row["page_url"] or "",
                ]
            )
        )
        for row in rows
    }

    framing_similarity = build_similarity_lookup(asset_texts, FRAMING_PROTOTYPES)
    cta_similarity = build_similarity_lookup(asset_texts, CTA_PROTOTYPES)
    audience_similarity = build_similarity_lookup(asset_texts, AUDIENCE_PROTOTYPES)

    conn = sqlite3.connect(DATABASE_PATH)
    try:
        conn.execute("delete from content_label_enrichment")

        for row in rows:
            asset_id = row["asset_id"]
            source_text = asset_texts[asset_id]
            tokens = tokenize(source_text)

            framing_scores = {
                label: framing_similarity[asset_id][label] + (keyword_score(tokens, KEYWORD_GROUPS[label]) * 0.2)
                for label in FRAMING_PROTOTYPES
            }
            cta_scores = {
                label: cta_similarity[asset_id][label] + (keyword_score(tokens, KEYWORD_GROUPS[label]) * 0.2)
                for label in CTA_PROTOTYPES
            }
            audience_scores = {
                label: audience_similarity[asset_id][label] + (keyword_score(tokens, KEYWORD_GROUPS[label]) * 0.2)
                for label in AUDIENCE_PROTOTYPES
            }

            derived_message_framing, message_confidence = top_label(framing_scores)
            derived_cta_style, cta_confidence = top_label(cta_scores)
            derived_audience_segment, audience_confidence = top_label(audience_scores)

            conn.execute(
                """
                insert into content_label_enrichment (
                    asset_id,
                    source_text,
                    token_count,
                    authority_score,
                    practical_score,
                    industry_specific_score,
                    conversion_score,
                    direct_conversion_score,
                    bridge_to_conversion_score,
                    nurture_capture_score,
                    high_intent_form_score,
                    women_in_finance_score,
                    client_facing_leaders_score,
                    promotion_readiness_score,
                    cross_audience_score,
                    derived_message_framing,
                    derived_cta_style,
                    derived_audience_segment,
                    message_framing_confidence,
                    cta_style_confidence,
                    audience_confidence,
                    framing_match_flag,
                    cta_match_flag,
                    audience_match_flag,
                    enrichment_version,
                    label_method,
                    updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'v1_text_rubric', 'rubric_plus_tfidf', current_timestamp)
                """,
                (
                    asset_id,
                    source_text,
                    len(tokens),
                    round(framing_scores["authority"], 4),
                    round(framing_scores["practical"], 4),
                    round(framing_scores["industry_specific"], 4),
                    round(framing_scores["conversion"], 4),
                    round(cta_scores["direct_conversion"], 4),
                    round(cta_scores["bridge_to_conversion"], 4),
                    round(cta_scores["nurture_capture"], 4),
                    round(cta_scores["high_intent_form"], 4),
                    round(audience_scores["women_in_finance"], 4),
                    round(audience_scores["client_facing_leaders"], 4),
                    round(audience_scores["promotion_readiness"], 4),
                    round(audience_scores["cross_audience"], 4),
                    derived_message_framing,
                    derived_cta_style,
                    derived_audience_segment,
                    message_confidence,
                    cta_confidence,
                    audience_confidence,
                    int(derived_message_framing == row["message_framing"]),
                    int(derived_cta_style == row["cta_style"]),
                    int(derived_audience_segment == row["audience_segment"]),
                ),
            )

        conn.commit()
    finally:
        conn.close()

    print(f"Enriched {len(rows)} content assets into {DATABASE_PATH}.")


if __name__ == "__main__":
    main()
