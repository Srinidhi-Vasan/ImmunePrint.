#Variables and Print
cancer_type = "glioblastoma"
num_genes = 200
print(cancer_type)
print(num_genes)

#Lists
genes = ["TP53", "EGFR", "KRAS", "MYC"]
print(genes[0]) #prints the first item
print(len(genes)) #print the number of items

#For Loops
for gene in genes:
    print("Gene found: ", gene)

#Reading a CSV File using pandas
import pandas as pd #This imports the pandas library and gives it a nickname called pd

data = {"gene": ["TP53", "EGFR"], "fold change": [3.2, 5.1]} #This creates a dictionary
df = pd.DataFrame(data) #This converts the dictionary into a actual table, called a dataframe
df.to_csv("my_genes.csv", index = False) 

df2 = pd.read_csv("my_genes.csv") #This reads the CSV back into a new dataframe
print(df2)

#Functions
def describe_gene(name, fold_change):
    if fold_change > 2:
        print(name, "is significantly upregulated")
    else:
        print(name, "is not significantly changed")

describe_gene("TP53", 3.2)
describe_gene("BRCA1", 1.1)