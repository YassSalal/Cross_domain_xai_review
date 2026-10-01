
# Cross-Domain Explainable AI: Coding Dataset and Analysis

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)


This repository contains the supplementary coding dataset and statistical
analysis scripts for the manuscript:

> **Salal, Y. K., Theodorou, P., & Sultan, H. S. (2026).** *Cross-Domain
> Explainable AI: A Unified Taxonomy, Metric Suitability Matrix, and
> Decision Framework for Classical ML, Vision, and LLMs.*

## Contents

| Path | Description |
|---|---|
| `data/Supplementary_Table_S1.csv` | Coding dataset: 125 sources × 9 variables |
| `docs/coding_protocol.md` | Coding manual and variable definitions |
| `analysis/statistical_tests.py` | Python script reproducing Tables 7 and 8 |
| `CITATION.cff` | Citation metadata for this repository |
| `LICENSE` | CC BY 4.0 license |

## Dataset Overview

The dataset codes **125 sources** cited in the manuscript across nine
variables: reference ID, short citation, domain, output form, metric
family, epistemic warrant score (EWS), maturity index (MI), and
metric–output alignment score (MOAS).

**Domain codes:**

- `CML` — Classical ML (n = 42)
- `CV` — Computer vision (n = 25)
- `NLP` — NLP / LLM (n = 46)
- `M/S` — Methodology / standards (n = 12, excluded from XAI analysis)

**Variables:**

- **EWS** (1–3): 1 = post-hoc rationalization/plausibility-only;
  2 = correlational/attribution-based; 3 = intervention-based causal evidence.
- **MI** (0–6): composite of methodological consensus (0–2),
  standardized evaluation metrics (0–2), and available tooling (0–2).
- **MOAS** (0–2): 0 = misaligned; 1 = partially aligned; 2 = aligned
  with the output-form-to-metric suitability matrix (Table 3).

## Reproducing the Analysis

```bash
git clone https://github.com/USERNAME/cross-domain-xai-review.git
cd cross-domain-xai-review
pip install pandas numpy scipy statsmodels
python analysis/statistical_tests.py
