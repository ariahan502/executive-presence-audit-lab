# Content Label Diagnostics Report v1

## Scope

This report summarizes the first text-derived labeling pass for the content registry.

The purpose is not to replace the manual taxonomy. The purpose is to test whether lightweight text-based enrichment changes how the funnel is segmented for growth analysis.

## Workflow

The current workflow combines:

- manual content taxonomy from `content_assets`
- text-derived framing / audience / CTA labels from `content_label_enrichment`
- synthetic performance outcomes from `content_performance`
- segment ranking outputs from both:
  - `growth_decision_ranking`
  - `enriched_growth_decision_ranking`

## Agreement snapshot

Across 9 content assets, the current text-derived enrichment agrees with the manual labels at the following rates:

- framing agreement: 0.778
- audience agreement: 0.889
- CTA agreement: 1.000

This is a healthy result for the current stage:

- CTA structure is already very clean and easily recoverable from text
- audience segmentation is mostly stable
- framing is the most ambiguous layer, which is exactly where a light NLP / LLM enhancement is most useful

## Main mismatches

### 1. `page_audit`

- manual framing: `authority`
- derived framing: `conversion`
- sessions: 8
- synthetic consultation lead rate: 0.0

Interpretation:

The text on the audit page is being read as a direct conversion asset rather than an upper-mid funnel authority asset. That is analytically useful because it suggests the page copy behaves more like a call-to-action page than a brand/credibility explainer.

Why it matters:

- manual taxonomy says this page belongs to an authority bucket
- text-derived taxonomy says it behaves like conversion-oriented copy
- this is exactly the kind of mismatch that could change segment-level reporting if more traffic were collected

### 2. `page_newsletter`

- manual framing: `practical`
- derived framing: `authority`
- sessions: 0

Interpretation:

This is a low-priority mismatch because the page has no tracked session volume yet. It is better treated as a taxonomy hygiene issue than a growth decision issue.

### 3. `page_consultation`

- manual audience: `cross_audience`
- derived audience: `women_in_finance`
- audience confidence: 0.0
- sessions: 0

Interpretation:

This is not a meaningful business signal. It is a tie-like edge case in a very small asset set, which actually helps the project because it gives a concrete example of why confidence thresholds matter before accepting model-derived labels.

## Ranking comparison

The top synthetic segments do not materially change between the manual and enriched views:

1. `client_facing_credibility` + `practical` + `bridge_to_conversion`
2. `women_in_finance` + `industry_specific` + `direct_conversion`
3. `women_in_finance` + `industry_specific` + `bridge_to_conversion`

The main change appears deeper in the ranking:

- manual ranking treats one executive-presence segment as `authority`
- enriched ranking reclassifies that lower-performing direct page segment as `conversion`

That is a useful outcome for the repo because it shows the enrichment layer can change how weaker or ambiguous assets are interpreted without disrupting the highest-signal segments.

## What this adds to the case study

This layer makes the project stronger as a growth DS portfolio piece because it now demonstrates:

- feature engineering from weakly structured text
- taxonomy validation rather than blind reliance on manual labels
- confidence-aware enrichment
- business interpretation of label disagreements
- a plausible handoff point for future LLM-assisted labeling

## Recommended next move

The next high-value step is not title generation or broader AI tooling.

The better next move is:

- add a confidence threshold for accepting derived labels in reporting
- compare manual-only vs enriched-only segment performance in one side-by-side report
- optionally run the exported prompt set through a real model and compare manual / rubric-derived / model-derived agreement
