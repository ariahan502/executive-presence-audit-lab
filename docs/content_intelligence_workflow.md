# Content Intelligence Workflow

## Purpose

This workflow adds a light NLP / LLM-ready layer to the project without changing the repo's main identity.

The goal is not content generation. The goal is to convert content metadata into structured signals that help answer growth questions such as:

- which message framings correlate with stronger downstream conversion quality
- whether manual content labels are internally consistent
- whether text-derived framing and CTA labels can enrich segmentation and modeling

## What the workflow includes

### 1. Manual taxonomy

The base registry in `app/content_registry.py` defines:

- content theme
- message framing
- audience segment
- CTA style

This is the ground-truth starting point for analysis.

### 2. Text-derived enrichment

`scripts/enrich_content_labels.py` creates `content_label_enrichment` by combining:

- keyword-rubric scores
- TF-IDF similarity to framing, CTA, and audience prototypes

It produces:

- derived framing label
- derived CTA-style label
- derived audience label
- confidence gaps between the top two label candidates
- match flags versus the manual labels

### 3. Diagnostics view

`content_label_diagnostics` compares the manual and derived labels and joins them back to synthetic content-performance metrics.

This is useful for:

- spotting taxonomy inconsistencies
- identifying assets whose framing is ambiguous
- deciding where richer LLM-assisted labeling might be most useful

### 4. LLM-ready prompt export

`scripts/export_llm_label_prompts.py` writes `analytics/content_label_prompts.jsonl`.

That file is designed as a handoff artifact for future model-based labeling. It keeps the project grounded in analytics by asking for:

- message framing
- audience segment
- CTA style
- one short note for conversion analysis

## Why this still fits growth DS

This layer supports:

- segmentation
- content performance analysis
- feature engineering
- lead-intent modeling
- decision support

It does not turn the repo into:

- a chatbot
- a title generator
- a generic AI content product

## Current state

At the moment, the enrichment layer is intentionally lightweight:

- manual registry remains the primary label source
- text-derived labels act as diagnostics and enrichment
- LLM usage is represented as a ready-to-run prompt workflow, not the center of the system

## Evaluation note

The current ablation results suggest the taxonomy layer is more useful for:

- lead-quality-weighted prioritization
- ambiguity resolution
- segment interpretation

than for improving pure classification AUC on the current synthetic dataset.

That is a good fit for the repo's growth DS positioning: the value of content intelligence here is not just predictive accuracy, but better prioritization of higher-quality downstream demand.
