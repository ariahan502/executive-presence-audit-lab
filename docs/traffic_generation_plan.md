# Traffic Generation Plan

## Purpose

This plan provides a lightweight way to seed enough local traffic to make segmented funnel analysis more useful.

## Recommended baseline

Generate at least 24-40 synthetic sessions before rerunning the segmented funnel report.

Suggested mix:

- finance-oriented consultation journeys
- client-facing consultation journeys
- article-to-newsletter journeys
- browse-only sessions

## Script

Use:

```bash
./.venv/bin/python scripts/seed_sample_traffic.py --sessions 30 --seed 42
./.venv/bin/python scripts/materialize_analytics.py
```

## What the script creates

The seeding script generates a mix of:

- article views
- page views
- CTA clicks
- newsletter form starts and submits
- consultation form starts and submits

It also varies:

- audience path
- UTM source, medium, and campaign
- job title
- industry
- company size
- lead goals and challenges

## Recommended workflow

1. Seed 30 sessions.
2. Rematerialize analytics views.
3. Rerun the main funnel queries.
4. Update `docs/segmented_funnel_report_v1.md` or create `v2` once the sample is large enough.

## Important note

This is synthetic validation traffic. It is useful for testing instrumentation, segmentation logic, and report structure, but it should not be mixed up with real production traffic in decision-making.

All seeded rows are now labeled with `traffic_type = synthetic`, while normal browser traffic defaults to `traffic_type = live`.
