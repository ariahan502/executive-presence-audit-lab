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
- `lead_scoring`
  - heuristic lead-quality scoring for consultation leads
- `lead_score_summary`
  - grouped quality summary by lead tier, content theme, and source

## Materialize the views

```bash
./.venv/bin/python scripts/materialize_analytics.py
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
from lead_scoring
where traffic_type = 'live'
order by lead_score desc, submitted_at desc;

select *
from lead_score_summary
where traffic_type = 'live'
order by avg_lead_score desc, leads desc;
```
