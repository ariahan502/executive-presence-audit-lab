# Segmented Funnel Report Live v1

Report date: 2026-05-12
Traffic filter: `traffic_type = 'live'`

## Scope

This report summarizes only live-tagged traffic from:

- `session_facts`
- `funnel_rollup`
- `path_performance`
- `lead_scoring`
- `lead_score_summary`

## Current live sample size

- Total live sessions: 2
- Live sessions with CTA click: 1
- Live sessions with consultation lead: 1
- Live sessions with newsletter signup: 0
- Live scored consultation leads: 2

## What the live data currently says

1. One live session entered an `executive_presence` path and produced a CTA click but no conversion.
2. One live session reached `/consultation-request` from a finance-related path and converted to a consultation lead.
3. Both live consultation leads currently score as `high` quality with scores of `82`.

## Interpretation

The live dataset is still too small for any reliable segment comparison.

What we can say:

- the live analytics pipeline is functioning
- live consultation capture is functioning
- live lead scoring is functioning

What we cannot say yet:

- which audience path converts better in real usage
- which acquisition source is stronger in real usage
- whether newsletter or consultation is the stronger real downstream action

## Recommended next step

Collect more real traffic after deployment and continue using `traffic_type = 'live'` as the default reporting filter.
