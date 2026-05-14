# Analytics Layer

This directory turns the app's operational tables into analysis-ready SQLite views.

The analytics layer now carries a `traffic_type` dimension so synthetic validation traffic can be separated from live traffic.

## Source tables

- `raw_events`
- `newsletter_signups`
- `consultation_leads`

## Models

- `session_facts`
  - one row per tracked session
  - includes first-touch dimensions, event counts, and conversion flags
- `funnel_rollup`
  - grouped funnel metrics by landing page, theme, framing, and acquisition source
- `path_performance`
  - grouped path summaries for simple path-to-conversion analysis
- `content_performance`
  - joins the content registry to session behavior for content/theme/framing comparisons
- `lead_scoring`
  - heuristic lead-quality scoring for consultation leads
- `lead_score_summary`
  - grouped quality summary by lead tier, content theme, and source
- `lead_intent_features`
  - session-level feature table for downstream consultation-intent modeling
- `growth_decision_ranking`
  - segment-level ranking across content theme, framing, audience, and CTA style for growth prioritization
- `content_label_diagnostics`
  - compares manual taxonomy labels with text-derived framing, audience, and CTA labels
- `enriched_growth_decision_ranking`
  - re-runs growth ranking logic using text-derived framing, audience, and CTA labels
- `content_label_comparison`
  - compares manual, text-derived, and model-assisted labels side by side
- `model_assisted_growth_decision_ranking`
  - re-runs growth ranking logic using model-assisted framing, audience, and CTA labels

## Materialize the views

```bash
./.venv/bin/python scripts/sync_content_assets.py
./.venv/bin/python scripts/enrich_content_labels.py
./.venv/bin/python scripts/import_model_assisted_labels.py
./.venv/bin/python scripts/materialize_analytics.py
./.venv/bin/python scripts/export_content_taxonomy.py
./.venv/bin/python scripts/train_lead_intent_model.py
./.venv/bin/python scripts/evaluate_feature_ablation.py
./.venv/bin/python scripts/export_llm_label_prompts.py
```

## Example queries

```sql
select * from session_facts where traffic_type = 'live' order by session_started_at desc limit 20;

select *
from funnel_rollup
where traffic_type = 'live'
order by consultation_lead_rate desc, sessions desc;

select *
from path_performance
where traffic_type = 'live'
order by sessions_with_consultation_lead desc, sessions desc;

select *
from content_performance
where traffic_type = 'live'
order by consultation_lead_rate desc, sessions desc;

select *
from growth_decision_ranking
where traffic_type = 'live'
order by segment_rank asc;

select *
from content_label_diagnostics
order by framing_match_flag asc, audience_match_flag asc, asset_id asc;

select *
from enriched_growth_decision_ranking
where traffic_type = 'live'
order by segment_rank asc;

select *
from content_label_comparison
order by manual_vs_model_framing_match asc, manual_vs_model_audience_match asc, asset_id asc;

select *
from model_assisted_growth_decision_ranking
where traffic_type = 'live'
order by segment_rank asc;

select *
from lead_scoring
where traffic_type = 'live'
order by lead_score desc, submitted_at desc;

select *
from lead_score_summary
where traffic_type = 'live'
order by avg_lead_score desc, leads desc;
```
