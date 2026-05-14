# Upgrade Blueprint v2

## Goal

Upgrade the project from a small funnel measurement prototype into a more differentiated growth DS case study centered on:

- content-to-conversion measurement
- qualified lead modeling
- content taxonomy and message framing
- growth decision support

The project should stay rooted in growth / ads DS rather than drift into a generic AI engineer or content-generation project.

## Core Positioning

The upgraded system is a:

- lead-quality measurement system
- content intelligence layer for conversion analysis
- growth decision-support workflow

It is not intended to become:

- a generic full-stack app
- a chatbot product
- a pure NLP demo
- a production-scale attribution platform

## Layer 1: Growth DS Core

Primary questions:

- Which audience/content entry paths produce higher-intent conversion behavior?
- Which content themes and message framings correlate with qualified demand?
- How should content and CTA strategy change when downstream conversion quality matters more than raw reach?

Core outputs:

- `session_facts`
- `funnel_rollup`
- `path_performance`
- `content_performance`
- live vs. synthetic reporting split

## Layer 2: DS / ML Enhancement

Primary modeling task:

- session-level lead-intent prediction

Modeling scope:

- use behavioral, source, path, and content-taxonomy features
- predict probability of downstream consultation conversion
- evaluate with baseline classification metrics

Current implementation target:

- baseline logistic regression
- reusable feature view: `lead_intent_features`
- exported session-level probability predictions

## Layer 3: Light NLP / LLM Enhancement

NLP/LLM should only support growth measurement.

Approved uses:

- content taxonomy
- message framing labels
- CTA-style labels
- optional content effectiveness labeling

Avoid as project center:

- title generation
- comment mining
- chatbot experiences
- freeform text generation as the main feature

## Upgrade Checklist

1. Centralize content metadata in a registry.
2. Persist content assets into a database table.
3. Add content taxonomy exports for analysis-ready labeling.
4. Add content-performance reporting views.
5. Add session-level lead-intent feature engineering.
6. Add a baseline lead-intent model with evaluation metrics.
7. Keep live-first reporting as the default for all decision-oriented analysis.

## Why This Does Not Overlap With The Other Repos

This repo should sell:

- content intelligence
- qualified lead modeling
- conversion-quality analytics

It should not compete with:

- ads measurement / uplift decisioning
- ranking / experimentation / retrieval systems

## Resume / Interview Outcome

After the upgrade, this repo should support claims about:

- conversion-oriented measurement design
- content and framing segmentation
- qualified lead modeling
- NLP/LLM-assisted content labeling as a feature layer
- growth decision-making grounded in downstream conversion quality
