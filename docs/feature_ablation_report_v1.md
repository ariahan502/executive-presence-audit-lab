# Feature Ablation and Prioritization Report v1

## Scope

This report evaluates whether content-taxonomy features materially improve lead-intent modeling and prioritization relative to a behavior/source/path baseline.

The current comparison uses four feature sets on the same holdout split:

1. `behavior_source_path`
2. `manual_taxonomy`
3. `text_derived_taxonomy`
4. `model_assisted_taxonomy`

## Validation setup

- synthetic sessions evaluated: 114
- validation sessions: 35
- validation positives: 18
- model family: logistic regression with holdout-based validation

## Main metrics

| Feature set | ROC AUC | PR AUC | Brier score | Top-decile capture | Precision@top-decile | Lead-score capture share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| behavior_source_path | 0.9967 | 0.9971 | 0.0349 | 0.2222 | 1.0000 | 0.2090 |
| manual_taxonomy | 0.9935 | 0.9940 | 0.0412 | 0.2222 | 1.0000 | 0.2449 |
| text_derived_taxonomy | 0.9935 | 0.9940 | 0.0411 | 0.2222 | 1.0000 | 0.2449 |
| model_assisted_taxonomy | 0.9935 | 0.9940 | 0.0411 | 0.2222 | 1.0000 | 0.2449 |

## Key takeaways

### 1. Behavior/source/path remains the strongest pure classifier

The baseline feature set still has the highest:

- ROC AUC
- PR AUC
- calibration quality via Brier score

Interpretation:

For this synthetic task, session behavior is already highly predictive of consultation conversion, so taxonomy features do not improve pure discrimination metrics.

### 2. Taxonomy features improve prioritization toward higher-quality leads

Even though AUC does not improve, the taxonomy-enriched models raise top-decile lead-score capture share from:

- `0.2090` to `0.2449`

That is:

- `+0.0359` absolute
- `+17.2%` relative

Interpretation:

The taxonomy layer is more valuable as a prioritization signal than as a raw classification gain. It helps the model surface a higher share of lead-quality-weighted outcomes among the top-ranked sessions.

### 3. Model-assisted labels do not yet outperform manual taxonomy on this dataset

The manual, text-derived, and model-assisted taxonomy variants currently produce identical prioritization metrics in the holdout evaluation.

Interpretation:

At the current project size, model-assisted labels behave more like a taxonomy validation layer than a source of large standalone performance gains.

## Segment-ordering effect

Comparing the three ranking views:

- `growth_decision_ranking`
- `enriched_growth_decision_ranking`
- `model_assisted_growth_decision_ranking`

The top 6 ranked synthetic segments remain stable.

The main ranking difference is a lower-ranked executive-presence direct-conversion segment:

- manual ranking: `authority`
- text-derived ranking: `conversion`
- model-assisted ranking: `conversion`

This means the labeling layers do not change the highest-signal priorities, but they do change how ambiguous lower-performing segments are interpreted.

## What this adds to the project

This pushes the repo closer to a stronger growth DS case study because it now demonstrates:

- feature ablation
- holdout-based model comparison
- calibration-aware evaluation
- lead-quality-weighted prioritization metrics
- manual vs weakly supervised vs model-assisted taxonomy comparison

## Practical conclusion

The current evidence suggests:

- behavior/source/path features are sufficient for strong conversion prediction
- taxonomy features are more useful for prioritizing higher-quality leads than for increasing pure AUC
- model-assisted labels are most useful for resolving ambiguous framing decisions, not for wholesale model replacement
