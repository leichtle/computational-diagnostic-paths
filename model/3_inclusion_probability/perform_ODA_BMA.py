import pandas as pd
from model.inclusion_probability.oda import oda_probit

# load data
mi_df = pd.read_csv('../imputation/results/')

# mi_df1 = pd.read_csv('../imputation/results/20140721000000-mi-imputation.csv', header=0)  # read data from csv
# mi_df2 = pd.read_csv('../imputation/results/20140721000001-mi-imputation.csv', header=0)  # read data from csv
# mi_df3 = pd.read_csv('../imputation/results/20140721000002-mi-imputation.csv', header=0)  # read data from csv

burnin_sim = 500
Gtot = 1000

xNames = ["ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "KA","LDH","NA.","TNT","UREA"]

# Test run for ICD-10 analogous to PIMA (MI_1)
print("Sanity check for mi 1:")
print(mi_df1.shape)
print(mi_df1.columns)

icd1Y = mi_df1["Klasse"]
icd1X = mi_df1[xNames]
oda_icd1 = oda_probit(xo=icd1X, zo=icd1Y, niter=Gtot, burnin=burnin_sim, lam_spec=1)

print("Results for mi 1:")
print(oda_icd1.incprob_rb)
print(oda_icd1.betabma)
print(oda_icd1.incprob)
print(oda_icd1.gamma)
print(oda_icd1.odds)
