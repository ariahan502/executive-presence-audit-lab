# Model-Assisted Label Comparison Report v1

## Purpose

This report compares three sources of content labels:

- manual taxonomy from `content_assets`
- text-derived labels from `content_label_enrichment`
- model-assisted labels from `content_label_model_assisted`

The goal is not to prove that one source is universally correct. The goal is to test whether a model-assisted pass helps validate or clarify conversion-oriented content segmentation.

## Agreement summary

Across the 9 content assets currently in the registry:

- manual vs text-derived framing agreement: 0.778
- manual vs model-assisted framing agreement: 0.889
- text-derived vs model-assisted framing agreement: 0.889

- manual vs text-derived audience agreement: 0.889
- manual vs model-assisted audience agreement: 1.000
- text-derived vs model-assisted audience agreement: 0.889

- manual vs text-derived CTA agreement: 1.000
- manual vs model-assisted CTA agreement: 1.000
- text-derived vs model-assisted CTA agreement: 1.000

## Main takeaways

### 1. CTA labels are already stable

All three sources agree on CTA structure for every asset.

Interpretation:

CTA style is the cleanest content-intelligence dimension in this project. It is already structured well enough that additional model complexity is not the highest-value upgrade area.

### 2. Audience labels are also mostly settled

The only meaningful disagreement between text-derived and the other two sources appears on `page_consultation`, where the text-derived method drifted toward `women_in_finance` while both manual and model-assisted labels stayed at `cross_audience`.

Interpretation:

This suggests the current rubric-plus-TF-IDF layer can occasionally over-index on local wording, while the model-assisted pass is better at preserving business-level interpretation.

### 3. Framing is the real ambiguity layer

The most important disagreement remains `page_audit`:

- manual framing: `authority`
- text-derived framing: `conversion`
- model-assisted framing: `conversion`

Interpretation:

The manual taxonomy treats the audit page as an authority asset, but both automated layers read it as conversion-oriented. That is analytically useful because it suggests the copy behaves more like a direct-response landing page than a pure credibility explainer.

### 4. `page_newsletter` shows the opposite pattern

- manual framing: `practical`
- text-derived framing: `authority`
- model-assisted framing: `practical`

Interpretation:

Here the model-assisted pass pulls the label back toward the manual interpretation and overrides a likely false positive from the text-derived layer.

## What this adds to the case study

This comparison strengthens the repo because it now demonstrates:

- manual taxonomy design
- weakly supervised text labeling
- model-assisted label validation
- confidence-aware disagreement analysis
- business interpretation of labeling differences

## Practical conclusion

If this were extended into a production workflow, the most reasonable policy would be:

- keep manual labels as the base taxonomy
- use text-derived labels as a low-cost diagnostic layer
- use model-assisted labels selectively for ambiguous framing decisions

That keeps the project grounded in growth analytics rather than turning it into a generic NLP system.
