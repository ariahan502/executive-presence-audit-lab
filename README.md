# Executive Presence Audit Lab

This is the shadow implementation for a content-to-lead growth funnel. It is intentionally scoped to support later work on:

- funnel analysis
- segmentation
- lead-quality scoring
- path analysis
- eventually, content taxonomy and NLP/LLM enrichment

## Current v1 scope

- Flask-based website with 6 core pages
- 3 article pages with distinct content themes
- newsletter signup form
- consultation request form
- local SQLite storage for submitted leads
- client-side anonymous/session/UTM capture

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project structure

```text
app/
  templates/
  static/
analytics/
  sql/
docs/
instance/
run.py
```

## Next build steps

1. Deploy and begin accumulating real traffic on the hosted app.
2. Use `traffic_type = 'live'` as the default reporting filter.
3. Decide whether SQLite remains sufficient or whether to move to Postgres after early live usage.

## Current analytics coverage

- `page_view` and `article_view` are sent from the browser to `/events`
- `cta_click` and form-start events are sent from the browser to `/events`
- `newsletter_submit` and `consultation_submit` are logged server-side into `raw_events`
- raw lead rows continue to persist in the dedicated signup/lead tables
- session and funnel views can be materialized from `analytics/sql/`
- consultation leads can now be scored with the `lead_scoring` view

## Analytics workflow

1. Run `./.venv/bin/python scripts/materialize_analytics.py`
2. Query the views in `analytics/sql/`
3. Use `session_facts` for session-level analysis
4. Use `funnel_rollup` for conversion and segmentation cuts
5. Use `path_performance` for early path analysis
6. Use `lead_scoring` and `lead_score_summary` for lead quality review

## Current report

- Live-only reporting guide: `docs/live_reporting_guide.md`
- Live-only funnel report: `docs/segmented_funnel_report_live_v1.md`
- First segmented funnel report: `docs/segmented_funnel_report_v1.md`
- Seeded synthetic-traffic report: `docs/segmented_funnel_report_v2.md`
- Traffic generation workflow: `docs/traffic_generation_plan.md`
- Render deployment runbook: `docs/render_deployment_runbook.md`
- Launch checklist: `docs/launch_checklist.md`
- Render preflight: `docs/render_preflight.md`
