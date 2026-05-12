# Executive Presence Audit Lab

A portfolio case study in building and instrumenting a content-to-lead funnel from end to end.

This project combines product thinking, event instrumentation, analytics modeling, and conversion analysis in a small Flask application designed around two outcomes: newsletter signup and consultation request.

## What This Demonstrates

- Built a 6-page Flask funnel with 3 audience/content entry points and 2 conversion paths
- Captured behavioral events including page views, article views, CTA clicks, form starts, and form submits
- Modeled session-level and funnel-level analytics in SQLite with 5 reusable reporting views
- Added heuristic lead scoring to rank consultation leads by audience fit, seniority, intent, and engagement
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
- `lead_scoring`
- `lead_score_summary`

## Current Project State

Application footprint:
- 6 core pages
- 3 article pages
- 2 form-based conversion flows
- 5 analytics views
- 1 Render deployment blueprint

Current reporting docs:
- live-only reporting guide: `docs/live_reporting_guide.md`
- live-only funnel report: `docs/segmented_funnel_report_live_v1.md`
- synthetic validation report: `docs/segmented_funnel_report_v2.md`
- deployment runbook: `docs/render_deployment_runbook.md`

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
./.venv/bin/python scripts/materialize_analytics.py
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
