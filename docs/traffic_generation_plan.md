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
- consultation-form abandonment sessions
- mixed exploration journeys that do not cleanly map to one funnel
- low-signal consultation submits and high-engagement non-submit sessions

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
- consultation form starts without submit
- multi-step mixed journeys with ambiguous intent

It also varies:

- audience path
- UTM source, medium, and campaign
- direct vs referred sessions
- referrer patterns
- job title
- industry
- company size
- lead goals and challenges

## Recommended workflow

1. Seed 30-50 sessions at a time.
2. Rematerialize analytics views.
3. Rerun the main funnel queries and `growth_decision_ranking`.
4. Retrain the baseline lead-intent model.
5. Update the funnel report or growth decision memo once the sample is large enough.

## Important note

This is synthetic validation traffic. It is useful for testing instrumentation, segmentation logic, and report structure, but it should not be mixed up with real production traffic in decision-making.

All seeded rows are now labeled with `traffic_type = synthetic`, while normal browser traffic defaults to `traffic_type = live`.

The seeding script also resumes counters from the existing database so repeated runs append new synthetic sessions rather than reusing the same session IDs.
