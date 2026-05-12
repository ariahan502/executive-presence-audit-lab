# Live Reporting Guide

## Default reporting rule

When reviewing funnel performance for real usage, always start with:

- `traffic_type = 'live'`

Synthetic seeded traffic should only be used for validation, QA, and scenario testing.

## Recommended live-first queries

### Live session summary

```sql
select *
from session_facts
where traffic_type = 'live'
order by session_started_at desc;
```

### Live funnel segments

```sql
select *
from funnel_rollup
where traffic_type = 'live'
order by consultation_lead_rate desc, newsletter_signup_rate desc, sessions desc;
```

### Live path performance

```sql
select *
from path_performance
where traffic_type = 'live'
order by sessions_with_consultation_lead desc, sessions desc;
```

### Live lead quality

```sql
select *
from lead_scoring
where traffic_type = 'live'
order by lead_score desc, submitted_at desc;
```

## Validation-only queries

Use these only when checking instrumentation or synthetic scenarios:

```sql
select *
from funnel_rollup
where traffic_type = 'synthetic'
order by sessions desc;
```

```sql
select *
from lead_score_summary
where traffic_type = 'synthetic'
order by avg_lead_score desc, leads desc;
```

## Current state

At the moment, the database contains both:

- a small amount of live-style test traffic
- a larger block of synthetic seeded traffic

That means any unfiltered query can still produce misleading conclusions.

## Safe interpretation rule

If a report does not explicitly filter by `traffic_type`, treat it as mixed traffic and do not use it for real performance decisions.
