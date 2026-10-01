Coding Protocol — Supplementary Table S1

This document describes the coding protocol used to produce
`data/Supplementary_Table_S1.csv`, which underlies Tables 7 and 8 of the
manuscript.

 1. Scope

The protocol was applied to the **125 sources** cited in the manuscript.
Twelve sources are methodological or regulatory documents and were coded
as `M/S`; they are excluded from the XAI-method analysis in Section 4.5.
The remaining **113 sources** constitute the empirical dataset.

 2. Coding Variables

 2.1 `ref_id`

Integer matching the reference number in the manuscript (1–125).

 2.2 `short_cite`

Abbreviated citation (author and year, or title fragment for non-authored
sources).

 2.3 `domain`

One of:

| Code | Meaning | n |
|---|---|---:|
| `CML` | Classical ML (tabular, ensemble, linear, tree) | 42 |
| `CV` | Computer vision (image, pixel, heatmap) | 25 |
| `NLP` | NLP / LLM (text, token, chain-of-thought) | 46 |
| `M/S` | Methodology or standards (excluded) | 12 |

Rule: assign the domain corresponding to the **primary modality** of the
source's method or evaluation. Surveys spanning multiple domains are
coded by their dominant contribution (e.g., Molnar 2022 → `CML`).

 2.4 `output_form`

The form of explanation the source produces or evaluates:

- `Feature attribution`
- `Rule`
- `Counterfactual`
- `Prototype`
- `Surrogate`
- `Natural language`
- `Attention map`
- `Attribution graph`
- `Concept vector`
- `Heatmap`
- `Multiple` (source discusses more than one)

 2.5 `metric_family`

The dominant evaluation metric family used:

- `Functional` — formal, automatic (fidelity, sparsity, sensitivity, completeness)
- `Human-based` — user studies, plausibility, satisfaction
- `Applied` — regulatory, audit, recourse
- `Multiple` — more than one family

2.6 `EWS` — Epistemic Warrant Score

| Value | Criterion |
|---:|---|
| 1 | Post-hoc rationalization or plausibility-only evidence; no causal validation |
| 2 | Correlational or attribution-based evidence; explanation correlated with output but no intervention |
| 3 | Intervention-based causal evidence explicitly reported in the source (e.g., ablation, activation patching, model editing, counterfactual intervention) |

Coding rule: if the source reports at least one intervention experiment
demonstrating causal necessity, code `3`. If it reports only attribution
or correlation, code `2`. If it evaluates plausibility or uses attention
weights without causal validation, code `1`.

2.7 `MI` — Maturity Index

Composite of three sub-scores, each 0–2:

| Sub-dimension | 0 | 1 | 2 |
|---|---|---|---|
| Methodological consensus | Contested | Emerging | Consolidated |
| Standardized metrics | None | Partial | Established |
| Available tooling | None | Research code | Maintained library |

Total range: 0–6. Coding rule: a source is "mature" on a sub-dimension
if multiple independent groups have adopted the method and its
evaluation. Consolidated methods (SHAP, LIME, Grad-CAM, Integrated
Gradients) score 5–6. Emerging methods (sparse autoencoders, activation
steering) score 3–4. Frontier methods (agentic explainers, circuit
tracing at scale) score 2–3.

 2.8 `MOAS` — Metric–Output Alignment Score

Coded against the suitability matrix in Table 3 of the manuscript.

| Value | Criterion |
|---:|---|
| 0 | Misaligned: the source's primary metric does not match the output form (e.g., fidelity applied to a natural-language explanation) |
| 1 | Partially aligned: the metric captures some but not all of the output form's epistemic claim (e.g., attention map evaluated by gradient correlation) |
| 2 | Aligned: the metric family matches the suitability matrix recommendation |

## 3. Coding Procedure

1. **Pilot round.** The protocol was applied to 15 randomly selected
   sources. Disagreements were resolved by discussion, and the coding
   manual was refined.

2. **Full coding.** All 125 sources were coded.

3. **Independent double-coding (planned).** A stratified subsample of
   30 sources (10 per domain) will be independently coded by two
   additional raters. Target agreement thresholds: Cohen's κ ≥ .85 for
   categorical variables; ICC(2,1) ≥ .85 for ordinal and composite
   variables. Until completed, values in this repository are
   **author-coded consensus values**.

4. **Consensus.** Disagreements are resolved by discussion; the
   consensus-coded dataset is used for analysis.

## 4. Known Limitations

- Coding was performed by the authors; independent double-coding is
  pending.
- The EWS scale compresses a continuum into three ordinal levels;
  boundary cases (attribution methods with partial intervention
  validation) may be coded conservatively as `2`.
- The MI composite weights the three sub-dimensions equally; alternative
  weightings may shift individual scores by ±1.
- The MOAS is defined against the manuscript's own suitability matrix,
  which is itself a contribution of the paper; using it as a coding
  criterion therefore embeds a degree of circularity that is
  acknowledged in Section 2.7 of the manuscript.

 5. Reproducibility

Run `analysis/statistical_tests.py` to regenerate Tables 7 and 8 from
the CSV. The script reports all descriptive statistics, hypothesis
tests, effect sizes, and confidence intervals.

 6. Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-10-01 | Initial release |
