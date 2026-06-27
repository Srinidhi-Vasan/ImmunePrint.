import pandas as pd

clinical = pd.read_csv("BRCA_clinicalMatrix", sep="\t", index_col=0)

# Find survival-related columns
survival_cols = [c for c in clinical.columns 
                 if any(word in c.lower() for word in 
                 ['vital', 'death', 'days', 'survival', 'status'])]

print("Survival-related columns:")
print(survival_cols)

# Show actual values in each of those columns
for col in survival_cols:
    print(f"\nColumn: {col}")
    print("Unique values:", clinical[col].unique()[:10])
    print("Non-null count:", clinical[col].notna().sum())