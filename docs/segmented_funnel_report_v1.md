# Segmented Funnel Report v1

Report date: 2026-05-12

## Scope

This report summarizes the first segmented funnel read from:

- `session_facts`
- `funnel_rollup`
- `path_performance`
- `lead_scoring`

The goal is to validate that the tracking and analytics pipeline is working and to capture any early directional insights.

## Current sample size

- Total tracked sessions: 2
- Sessions with CTA click: 1
- Sessions with consultation lead: 1
- Sessions with newsletter signup: 0
- Scored consultation leads: 2

This is not enough volume for a reliable performance conclusion. It is enough to confirm that the funnel instrumentation, session modeling, and lead scoring layers are working end to end.

## Segment summary

### By landing page and acquisition

1. `linkedin / social / spring_test` drove one tracked session into the `executive_presence` path.
   - Result: CTA click observed
   - Conversion: no newsletter signup, no consultation lead

2. `google / cpc / finance_search` drove one tracked session into the consultation path.
   - Result: consultation lead captured
   - Conversion rate in current sample: 100%

### By content theme

1. `executive_presence`
   - 1 session
   - 1 CTA click
   - 0 downstream conversions

2. `consultation`
   - 1 session
   - 1 consultation lead
   - no upstream browsing captured in that tracked session

### By path

1. `/for-women-in-finance > /consultation-request`
   - 1 session
   - 1 consultation lead
   - 100% consultation conversion in current sample

2. `(no path recorded)`
   - 1 session
   - 1 CTA click
   - 0 conversions

## Lead quality summary

Both current consultation leads scored `82` and landed in the `high` tier.

Observed common characteristics:

- industry: Finance
- company size: `201-1000`
- role seniority: `Director` or `VP`
- goal language tied to leadership or executive readiness
- acquisition source: Google CPC
- audience-fit path includes `/for-women-in-finance`

## Early interpretation

The strongest early directional signal is not about broad funnel performance yet. It is that the finance-oriented path currently aligns with the highest-intent leads in the sample.

That said, the sample is too small to conclude:

- whether Google CPC is actually better than LinkedIn social
- whether the women-in-finance path is genuinely higher converting
- whether consultation intent is stronger than newsletter intent overall

## What this tells us

1. The instrumentation is working well enough to support segmented analysis.
2. The women-in-finance path is currently the clearest hypothesis to keep testing.
3. The newsletter path has no observed conversions yet, so it needs more traffic before it can be evaluated.
4. Lead scoring is producing interpretable outputs and can now be used alongside conversion metrics.

## Recommended next actions

1. Generate at least 20-30 more sessions across the main audience paths before comparing conversion rates.
2. Intentionally drive traffic into both `/for-women-in-finance` and `/for-client-facing-leaders` so the audience comparison becomes meaningful.
3. Ensure at least a few sessions include article views before consultation so path analysis reflects the content-led funnel design.
4. Decide whether the newsletter path should remain a secondary conversion or receive stronger CTA placement.
