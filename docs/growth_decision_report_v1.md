# Growth Decision Report v1

## Scope

This report summarizes the upgraded synthetic-validation layer after:

- expanding the traffic seeding mix with noisier journeys
- adding content taxonomy and message-framing metadata
- adding `growth_decision_ranking`
- retraining the baseline lead-intent model

This is still a synthetic decision-support readout, not a live production performance report.

## Dataset snapshot

- synthetic sessions in `lead_intent_features`: 114
- synthetic positive consultation sessions: 58
- baseline lead-intent holdout metrics:
  - validation ROC AUC: 0.9935
  - validation PR AUC: 0.9940

The model is still very strong because the dataset is generated and the segment structure remains cleaner than real traffic, but it is no longer perfectly separable after the addition of contradictory paths and abandonment cases.

## Top-ranked segments

Using `growth_decision_ranking`, the strongest synthetic segments currently are:

1. `client_facing_credibility` + `practical` + `client_facing_leaders` + `bridge_to_conversion`
   - 27 sessions
   - consultation lead rate: 0.926
   - average lead score: 79.32
   - decision score: 80.46
2. `women_in_finance` + `industry_specific` + `women_in_finance` + `direct_conversion`
   - 29 sessions
   - consultation lead rate: 0.897
   - average lead score: 88.50
   - decision score: 80.34
3. `women_in_finance` + `industry_specific` + `women_in_finance` + `bridge_to_conversion`
   - 20 sessions
   - consultation lead rate: 0.300
   - average lead score: 86.50
   - decision score: 58.45

## Main readouts

- Direct conversion pages are still strongest for high-intent outcomes, especially for `women_in_finance`.
- Article-led client-facing journeys remain the cleanest bridge-to-conversion path and now rank first when both conversion rate and lead quality are weighted together.
- `executive_presence` / `authority` content still underperforms as a direct decision-driving segment in the synthetic mix, which suggests it works better as an upper-funnel or nurture entry point than as a high-intent closer.
- The gap between `women_in_finance` direct conversion and `women_in_finance` bridge-to-conversion is now visible in the ranking layer, which is exactly the kind of content/CTA decision split this project should surface.

## Why this matters for the project

This upgrade makes the repo more defensible as a growth DS case study because it now has:

- explicit content taxonomy
- segment-level conversion-quality ranking
- non-trivial negative and contradictory journey patterns
- a baseline predictive layer tied to qualified consultation outcomes

## Next recommended upgrade

The next highest-value step is to add one more layer of content intelligence:

- enrich content assets with a tighter framing schema
- optionally add lightweight NLP/LLM-assisted labels for message framing or CTA style
- compare whether manual vs enriched labels improve segment separation or model usefulness
