import pandas as pd
from model.c_inclusion_probability.oda import oda_probit


def perform_oda(df, burnin_sim = 500, g_tot = 1000):

    xNames = ["ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "KA","LDH","NA.","TNT","UREA"]

    # Test run for ICD-10 analogous to PIMA
    print("Sanity check:")
    print(df.shape)
    print(df.columns)

    icd1_y = df["I200_I2519"]
    icd1_x = df[xNames]
    oda_icd1 = oda_probit(xo=icd1_x, zo=icd1_y, niter=g_tot, burnin=burnin_sim, lam_spec=1)

    print("Results:")
    print(oda_icd1["incprob_rb"])
    print(oda_icd1["betama"])
    print(oda_icd1["incprob"])
    print(oda_icd1["gamma"])
    print(oda_icd1["odds"])


if __name__ == "__main__":
    # load data
    mi_df = pd.read_csv('../b_add_label_row/results/20181003161605-mi-imputation+label.csv')
    # mi_df1 = pd.read_csv('../imputation/results/20140721000000-mi-imputation.csv', header=0)  # read data from csv
    # mi_df2 = pd.read_csv('../imputation/results/20140721000001-mi-imputation.csv', header=0)  # read data from csv
    # mi_df3 = pd.read_csv('../imputation/results/20140721000002-mi-imputation.csv', header=0)  # read data from csv
    perform_oda(mi_df)
