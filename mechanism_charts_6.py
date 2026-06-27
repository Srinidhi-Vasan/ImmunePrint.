import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from lifelines.statistics import logrank_test

# ── Load data ──────────────────────────────────────────────────
scores = pd.read_csv("evasion_scores.csv", index_col=0)
clinical = pd.read_csv("BRCA_clinicalMatrix", sep="\t", index_col=0)

# ── Match and clean survival data ──────────────────────────────
common = scores.index.intersection(clinical.index)
scores = scores.loc[common]
clinical = clinical.loc[common]

clinical["duration"] = pd.to_numeric(
    clinical["days_to_death"], errors="coerce"
).fillna(pd.to_numeric(clinical["days_to_last_followup"], errors="coerce"))
clinical["event"] = (clinical["vital_status"] == "DECEASED").astype(int)

valid = clinical[["duration", "event"]].dropna()
valid = valid[valid["duration"] > 0]
scores = scores.loc[valid.index]
clinical = clinical.loc[valid.index]

# ── Calculate p-value for each mechanism ──────────────────────
mechanisms = [
    "Checkpoint Upregulation",
    "MHC Downregulation",
    "T-cell Exclusion",
    "Immunosuppressive Cytokines",
    "Regulatory T-cell Recruitment"
]

pvalues = {}
median_diffs = {}

for mech in mechanisms:
    if mech not in scores.columns:
        continue

    med = scores[mech].median()
    high = [i for i in scores[scores[mech] >= med].index if i in valid.index]
    low = [i for i in scores[scores[mech] < med].index if i in valid.index]

    if len(high) < 10 or len(low) < 10:
        continue

    res = logrank_test(
        clinical.loc[high, "duration"],
        clinical.loc[low, "duration"],
        event_observed_A=clinical.loc[high, "event"],
        event_observed_B=clinical.loc[low, "event"]
    )
    pvalues[mech] = res.p_value

    high_med = clinical.loc[high, "duration"].median()
    low_med = clinical.loc[low, "duration"].median()
    median_diffs[mech] = high_med - low_med

# ── Plot 1: P-value bar chart ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

mechs = list(pvalues.keys())
pvals = list(pvalues.values())
colors = ["#e74c3c" if p < 0.05 else "#95a5a6" for p in pvals]

bars = axes[0].barh(mechs, pvals, color=colors)
axes[0].axvline(x=0.05, color="black", linestyle="--",
                linewidth=1.5, label="p=0.05 threshold")
axes[0].set_xlabel("P-value (lower = more significant)")
axes[0].set_title("Which Evasion Mechanism\nPredicts Survival?", 
                   fontweight="bold")
axes[0].legend()

red_patch = mpatches.Patch(color="#e74c3c", label="Significant (p<0.05)")
grey_patch = mpatches.Patch(color="#95a5a6", label="Not significant")
axes[0].legend(handles=[red_patch, grey_patch])

# Add p-value labels on bars
for bar, pval in zip(bars, pvals):
    axes[0].text(
        bar.get_width() + 0.002,
        bar.get_y() + bar.get_height() / 2,
        f"p={pval:.3f}",
        va="center", fontsize=9
    )

# ── Plot 2: Survival difference bar chart ────────────────────
diffs = [median_diffs[m] for m in mechs]
diff_colors = ["#e74c3c" if d < 0 else "#2ecc71" for d in diffs]

axes[1].barh(mechs, diffs, color=diff_colors)
axes[1].axvline(x=0, color="black", linewidth=1)
axes[1].set_xlabel("Median Survival Difference (days)\nHigh vs Low Evasion")
axes[1].set_title("Survival Impact of Each\nEvasion Mechanism", 
                   fontweight="bold")

red_patch2 = mpatches.Patch(
    color="#e74c3c", 
    label="High evasion = shorter survival"
)
green_patch2 = mpatches.Patch(
    color="#2ecc71", 
    label="High evasion = longer survival"
)
axes[1].legend(handles=[red_patch2, green_patch2])

plt.suptitle(
    "Immune Evasion Mechanisms in Breast Cancer — TCGA Analysis",
    fontsize=13, fontweight="bold", y=1.02
)
plt.tight_layout()
plt.savefig("mechanism_analysis.png", bbox_inches="tight", dpi=150)
plt.show()

print("Saved mechanism_analysis.png")
print("\nP-value summary:")
for mech, p in sorted(pvalues.items(), key=lambda x: x[1]):
    sig = "✓ SIGNIFICANT" if p < 0.05 else ""
    print(f"  {mech}: {p:.4f} {sig}")