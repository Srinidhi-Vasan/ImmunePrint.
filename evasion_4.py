import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────
df = pd.read_csv("HiSeqV2.csv", sep="\t", index_col=0)

# ── Separate tumor vs normal samples ───────────────────────────
# TCGA patient IDs encode sample type in characters 14-15
# 01 = primary tumor, 11 = normal tissue
tumor_cols = [c for c in df.columns if c[13:15] == '01']
normal_cols = [c for c in df.columns if c[13:15] == '11']

print(f"Tumor samples: {len(tumor_cols)}")
print(f"Normal samples: {len(normal_cols)}")

tumor_df = df[tumor_cols]
normal_df = df[normal_cols]

# ── Define your 5 immune evasion gene sets ─────────────────────
# These are well-established genes for each mechanism
# You will cite published immune evasion literature for these

evasion_genes = {
    "Checkpoint Upregulation": [
        "CD274",    # PD-L1
        "PDCD1LG2", # PD-L2
        "CTLA4",
        "HAVCR2",   # TIM-3
        "LAG3",
        "TIGIT"
    ],
    "MHC Downregulation": [
        "HLA-A", "HLA-B", "HLA-C",
        "B2M",
        "TAP1", "TAP2"
    ],
    "T-cell Exclusion": [
        "TGFB1", "TGFB2",
        "CXCL12",
        "VEGFA",
        "WNT5A"
    ],
    "Immunosuppressive Cytokines": [
        "IL10",
        "TGFB1",
        "VEGFA",
        "IL6",
        "CCL2"
    ],
    "Regulatory T-cell Recruitment": [
        "FOXP3",
        "IL2RA",
        "CCL22",
        "CCL17",
        "IKZF2"
    ]
}

# ── Extract and score each mechanism ───────────────────────────
results = {}

for mechanism, genes in evasion_genes.items():
    # Keep only genes that actually exist in our dataset
    available_genes = [g for g in genes if g in df.index]
    missing = [g for g in genes if g not in df.index]
    
    print(f"\n{mechanism}")
    print(f"  Available: {available_genes}")
    if missing:
        print(f"  Missing from dataset: {missing}")
    
    if available_genes:
        # Mean expression across the gene set per patient
        mechanism_score = tumor_df.loc[available_genes].mean(axis=0)
        results[mechanism] = mechanism_score

# ── Build patient-level evasion score table ────────────────────
scores_df = pd.DataFrame(results)
scores_df.index.name = "patient_id"

print("\nEvasion scores table (first 5 patients):")
print(scores_df.head())

print("\nShape:", scores_df.shape)

# ── Normalize scores to 0-10 scale (easier to interpret) ───────
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 10))
scores_normalized = pd.DataFrame(
    scaler.fit_transform(scores_df),
    columns=scores_df.columns,
    index=scores_df.index
)

# Add composite overall disguise score (average of all mechanisms)
scores_normalized["Overall_Disguise_Score"] = scores_normalized.mean(axis=1)

print("\nNormalized scores (first 5 patients):")
print(scores_normalized.head())

# ── Save ───────────────────────────────────────────────────────
scores_normalized.to_csv("evasion_scores.csv")
print("\nSaved to evasion_scores.csv")