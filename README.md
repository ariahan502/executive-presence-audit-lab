# Executive Presence Audit Lab

A growth analytics case study in building a measured content-to-conversion funnel with lead-quality modeling and light content intelligence.

This project combines product thinking, event instrumentation, analytics modeling, and conversion analysis in a small Flask application designed around two outcomes: newsletter signup and consultation request. The current upgrade path pushes the repo beyond a simple funnel app into a more differentiated growth DS case study: content taxonomy, message-framing-aware reporting, qualified-conversion analysis, and a baseline lead-intent model.

## What This Demonstrates

- Built a 6-page Flask funnel with 3 audience/content entry points and 2 conversion paths
- Captured 7 behavioral event types including page views, article views, CTA clicks, form starts, and form submits
- Modeled session-level, path-level, content-level, decision-ranking, and multi-source label diagnostics analytics in SQLite with 12 reusable reporting views
- Added a manual content taxonomy layer for theme, framing, audience, and CTA structure
- Added text-derived content labeling, model-assisted label comparison, and an LLM-ready prompt export workflow for framing, audience, and CTA enrichment
- Added heuristic lead scoring and a baseline lead-intent modeling workflow for qualified-conversion analysis
- Separated `live` and `synthetic` traffic so validation data does not contaminate real reporting
- Prepared the app for first deployment on Render with persistent storage

## Funnel Structure

Primary conversion:
- consultation request

Secondary conversion:
- newsletter signup

Audience/content paths:
- women in finance
- client-facing leaders
- executive presence / promotion signals

## Analytics Coverage

Tracked events:
- `page_view`
- `article_view`
- `cta_click`
- `newsletter_form_start`
- `newsletter_submit`
- `consultation_form_start`
- `consultation_submit`

Analytics views:
- `session_facts`
- `funnel_rollup`
- `path_performance`
- `content_performance`
- `lead_scoring`
- `lead_score_summary`
- `lead_intent_features`
- `growth_decision_ranking`
- `content_label_diagnostics`
- `enriched_growth_decision_ranking`
- `content_label_comparison`
- `model_assisted_growth_decision_ranking`

Content intelligence layer:
- `content_assets` registry for content theme, audience, message framing, funnel-stage intent, and CTA style
- taxonomy export to `analytics/content_taxonomy_snapshot.csv`
- text-derived label enrichment in `content_label_enrichment`
- model-assisted labels in `content_label_model_assisted`
- LLM-ready labeling prompts in `analytics/content_label_prompts.jsonl`
- baseline lead-intent predictions export to `analytics/lead_intent_predictions.csv`
- feature ablation results in `analytics/feature_ablation_results.csv`

## Current Project State

Application footprint:
- 6 core pages
- 3 article pages
- 2 form-based conversion flows
- 12 analytics views
- 1 content taxonomy registry
- 1 content-label enrichment workflow
- 1 model-assisted label comparison workflow
- 1 baseline lead-intent training script
- 1 feature-ablation evaluation workflow
- 1 Render deployment blueprint

Current reporting docs:
- live-only reporting guide: `docs/live_reporting_guide.md`
- live-only funnel report: `docs/segmented_funnel_report_live_v1.md`
- synthetic validation report: `docs/segmented_funnel_report_v2.md`
- synthetic decision report: `docs/growth_decision_report_v1.md`
- content intelligence workflow: `docs/content_intelligence_workflow.md`
- content label diagnostics report: `docs/content_label_diagnostics_report_v1.md`
- model-assisted label comparison report: `docs/model_assisted_label_comparison_report_v1.md`
- feature ablation report: `docs/feature_ablation_report_v1.md`
- deployment runbook: `docs/render_deployment_runbook.md`
- upgrade blueprint: `docs/upgrade_blueprint_v2.md`

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Analytics Workflow

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

Use `traffic_type = 'live'` as the default filter for any real performance reporting.

## Deployment

The repo includes:
- `render.yaml`
- `Procfile`
- persistent-disk SQLite configuration
- launch and preflight docs in `docs/`

## Repo Structure

```text
app/
  templates/
  static/
analytics/
  sql/
docs/
scripts/
run.py
render.yaml
```
