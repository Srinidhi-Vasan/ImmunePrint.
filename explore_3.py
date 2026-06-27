import pandas as pd

#Load the gene expression data
#sep = "\t" means columns are separated by tabs, not commas
#index_col = 0, means the first column (gene names) becomes the row labels
df = pd.read_csv("HiSeqV2.csv", sep = "\t", index_col = 0)

#How big is this table?
print("Number of genes(rows):", df.shape[0])
print("Number of patients (columns)):", df.shape[1])

#Show first 5 rows and columns
print("\nFirst 5 genes, first 5 patients:")
print(df.iloc[:5, :5])

#Show some gene names
print("\nSome gene names:")
print(df.index[:10].tolist())

#Show some patient IDs
print("\nSome patient IDs:")
print(df.columns[:5].tolist())

# Load clinical data
clinical = pd.read_csv("BRCA_clinicalMatrix", sep="\t", index_col=0)

print("\nClinical data shape:", clinical.shape)
print("\nAvailable clinical columns:")
print(clinical.columns.tolist())

# Check if survival data exists
survival_cols = [c for c in clinical.columns if 'survival' in c.lower() or 'vital' in c.lower() or 'days' in c.lower()]
print("\nSurvival-related columns found:")
print(survival_cols)