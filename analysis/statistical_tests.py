"""
Statistical analysis for Supplementary Table S1.

Reproduces Table 7 (distribution of EWS, MI, MOAS by domain) and
Table 8 (hypothesis tests) of:

    Salal, Theodorou, & Sultan (2026). Cross-Domain Explainable AI:
    A Unified Taxonomy, Metric Suitability Matrix, and Decision
    Framework for Classical ML, Vision, and LLMs.

Usage:
    pip install pandas numpy scipy statsmodels
    python statistical_tests.py

Outputs:
    - Descriptive statistics for EWS, MI, MOAS by domain
    - Kruskal-Wallis test for EWS by domain with Dunn post-hoc
    - Ordinal regression for MI by domain
    - Logistic regression for MOAS predicting evaluation rigor
    - Mann-Whitney U for CoT vs. mechanistic interpretability on EWS
"""

import os
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel

# ---------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "data", "Supplementary_Table_S1.csv")

df = pd.read_csv(CSV_PATH)

# Exclude methodology/standards sources
xai = df[df["domain"].isin(["CML", "CV", "NLP"])].copy()
xai["domain"] = pd.Categorical(
    xai["domain"], categories=["CML", "CV", "NLP"], ordered=True
)

print(f"Total sources: {len(df)}")
print(f"XAI sources (analysis set): {len(xai)}")
print()

# ---------------------------------------------------------------------
# 2. Table 7 — Descriptive statistics
# ---------------------------------------------------------------------

print("=" * 70)
print("TABLE 7. Distribution of EWS, MI, and MOAS by domain")
print("=" * 70)

def summarize(group):
    n = len(group)
    ews_mean = group["EWS"].mean()
    ews_sd = group["EWS"].std(ddof=1)
    ews_med = group["EWS"].median()
    ews_q1 = group["EWS"].quantile(0.25)
    ews_q3 = group["EWS"].quantile(0.75)
    ews3 = (group["EWS"] == 3).mean() * 100
    ews2 = (group["EWS"] == 2).mean() * 100
    ews1 = (group["EWS"] == 1).mean() * 100
    mi_mean = group["MI"].mean()
    mi_sd = group["MI"].std(ddof=1)
    mi_med = group["MI"].median()
    mi_q1 = group["MI"].quantile(0.25)
    mi_q3 = group["MI"].quantile(0.75)
    moas2 = (group["MOAS"] == 2).mean() * 100
    moas1 = (group["MOAS"] == 1).mean() * 100
    moas0 = (group["MOAS"] == 0).mean() * 100
    return pd.Series({
        "n": n,
        "EWS_mean": round(ews_mean, 2),
        "EWS_SD": round(ews_sd, 2),
        "EWS_median": ews_med,
        "EWS_IQR": f"({ews_q1:.0f}-{ews_q3:.0f})",
        "EWS3_%": round(ews3, 1),
        "EWS2_%": round(ews2, 1),
        "EWS1_%": round(ews1, 1),
        "MI_mean": round(mi_mean, 2),
        "MI_SD": round(mi_sd, 2),
        "MI_median": mi_med,
        "MI_IQR": f"({mi_q1:.0f}-{mi_q3:.0f})",
        "MOAS_aligned_%": round(moas2, 1),
        "MOAS_partial_%": round(moas1, 1),
        "MOAS_misaligned_%": round(moas0, 1),
    })

by_domain = xai.groupby("domain", observed=True).apply(summarize)
overall = summarize(xai).rename("Overall")
table7 = pd.concat([by_domain, overall.to_frame().T])
print(table7.to_string())
print()

# ---------------------------------------------------------------------
# 3. Table 8 — Hypothesis tests
# ---------------------------------------------------------------------

print("=" * 70)
print("TABLE 8. Hypothesis tests")
print("=" * 70)

# --- H1: Kruskal-Wallis for EWS by domain ---
groups = [g["EWS"].values for _, g in xai.groupby("domain", observed=True)]
H, p_kw = stats.kruskal(*groups)
k = len(groups)
n_total = len(xai)
eps2 = (H - k + 1) / (n_total - k)  # epsilon-squared effect size
print(f"H1: Kruskal-Wallis EWS by domain")
print(f"    H({k-1}) = {H:.2f}, p = {p_kw:.4f}, epsilon^2 = {eps2:.2f}")
print()

# --- H1a-c: Dunn post-hoc with Bonferroni ---
def dunn_posthoc(xai):
    """Dunn's post-hoc test for Kruskal-Wallis with Bonferroni correction."""
    from scipy.stats import rankdata
    xai = xai.copy()
    xai["rank"] = rankdata(xai["EWS"])
    domain_ranks = xai.groupby("domain", observed=True)["rank"].mean()
    n_i = xai.groupby("domain", observed=True).size()
    N = len(xai)
    # Tie correction
    _, counts = np.unique(xai["EWS"], return_counts=True)
    tie_corr = np.sum(counts ** 3 - counts) / (12 * (N - 1))
    sigma2 = N * (N + 1) / 12 - tie_corr

    results = []
    domains = list(domain_ranks.index)
    for i in range(len(domains)):
        for j in range(i + 1, len(domains)):
            di, dj = domains[i], domains[j]
            diff = abs(domain_ranks[di] - domain_ranks[dj])
            se = np.sqrt(sigma2 * (1 / n_i[di] + 1 / n_i[dj]))
            z = diff / se
            p_raw = 2 * (1 - stats.norm.cdf(z))
            p_bonf = min(p_raw * 3, 1.0)  # 3 pairwise comparisons
            results.append((di, dj, z, p_bonf))
    return results

print("H1a-c: Dunn post-hoc (Bonferroni-corrected, 3 comparisons)")
for di, dj, z, p in dunn_posthoc(xai):
    print(f"    {di} vs {dj}: z = {z:.2f}, p = {p:.4f}")
print()

# --- H2: Ordinal regression for MI by domain ---
# Recode domain as numeric for ordinal regression
xai["domain_num"] = xai["domain"].cat.codes  # CML=0, CV=1, NLP=2
X = sm.add_constant(xai[["domain_num"]])
y = xai["MI"]
model_mi = OrderedModel(y, X, distr="logit").fit(method="bfgs", disp=False)
print("H2: Ordinal regression MI ~ domain")
print(model_mi.summary().tables[1])
print(f"    Pseudo-R^2 (McFadden): {1 - model_mi.llf / model_mi.llnull:.2f}")
print()

# --- H3: Logistic regression for MOAS predicting evaluation rigor ---
# Define "evaluation rigor" as MI >= median (proxy for rigor)
median_mi = xai["MI"].median()
xai["rigor_high"] = (xai["MI"] >= median_mi).astype(int)
X3 = sm.add_constant(xai[["MOAS"]])
model_logit = sm.Logit(xai["rigor_high"], X3).fit(disp=False)
print("H3: Logistic regression (rigor_high ~ MOAS)")
print(model_logit.summary().tables[1])
print()

# --- H4: Mann-Whitney U for CoT vs. mechanistic interpretability ---
# Identify CoT sources (natural language output, NLP domain, plausibility-prone)
cot_ids = [4, 21, 34, 49, 88, 89, 90, 104, 124]  # CoT-related
mech_ids = [9, 15, 28, 48, 80, 81, 85, 98, 99, 100, 101]  # mechanistic

cot_ews = df[df["ref_id"].isin(cot_ids)]["EWS"].values
mech_ews = df[df["ref_id"].isin(mech_ids)]["EWS"].values

U, p_mw = stats.mannwhitneyu(cot_ews, mech_ews, alternative="less")
# Rank-biserial correlation
n1, n2 = len(cot_ews), len(mech_ews)
r_rb = 1 - (2 * U) / (n1 * n2)
print(f"H4: Mann-Whitney U CoT (n={n1}) vs. mechanistic (n={n2}) on EWS")
print(f"    U = {U:.1f}, p = {p_mw:.4f}, r = {r_rb:.2f}")
print(f"    CoT median EWS: {np.median(cot_ews):.1f} (IQR {np.percentile(cot_ews,25):.0f}-{np.percentile(cot_ews,75):.0f})")
print(f"    Mechanistic median EWS: {np.median(mech_ews):.1f} (IQR {np.percentile(mech_ews,25):.0f}-{np.percentile(mech_ews,75):.0f})")
print()

# ---------------------------------------------------------------------
# 4. Save outputs
# ---------------------------------------------------------------------

out_dir = os.path.join(HERE, "output")
os.makedirs(out_dir, exist_ok=True)
table7.to_csv(os.path.join(out_dir, "Table7.csv"))
print(f"Table 7 saved to {out_dir}/Table7.csv")
