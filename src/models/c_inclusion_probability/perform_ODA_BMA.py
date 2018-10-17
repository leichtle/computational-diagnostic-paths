import pandas as pd
from model.c_inclusion_probability.oda import oda_probit


def perform_oda(df, burnin_sim=500, g_tot=1000):

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

    #print(oda_icd1["betama"])
    #print(oda_icd1["incprob"])
    #print(oda_icd1["gamma"])
    #print(oda_icd1["odds"])


if __name__ == "__main__":
    # load data
    #mi_df = pd.read_csv('../b_add_label_row/results/20181003161605-mi-imputation+label.csv')
    # mi_df1 = pd.read_csv('../a_imputation/results/20140721000000-mi-imputation.csv', header=0)  # read data from csv
    # mi_df2 = pd.read_csv('../a_imputation/results/20140721000001-mi-imputation.csv', header=0)  # read data from csv
    # mi_df3 = pd.read_csv('../a_imputation/results/20140721000002-mi-imputation.csv', header=0)  # read data from csv

    # load data
    dataMatrix = pd.read_csv("../a_imputation/results/20140721000000_mi_comb_20_iter.csv")
    dataMatrix1 = dataMatrix[["ALAT.1","AP.1","ASAT.1","CA.1","CK.1","CREA.1","CRP.1","GGT.1","GL.1","I200_I2519","KA.1","LDH.1","NA.1","TNT.1","UREA.1"]]
    dataMatrix1.columns = ["ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA"]

    dataMatrix2 = dataMatrix[["ALAT.2","AP.2","ASAT.2","CA.2","CK.2","CREA.2","CRP.2","GGT.2","GL.2","I200_I2519","KA.2","LDH.2","NA.2","TNT.2","UREA.2"]]
    dataMatrix2.columns = ["ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA"]

    dataMatrix3 = dataMatrix[["ALAT.3","AP.3","ASAT.3","CA.3","CK.3","CREA.3","CRP.3","GGT.3","GL.3","I200_I2519","KA.3","LDH.3","NA.3","TNT.3","UREA.3"]]
    dataMatrix3.columns = ["ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA"]

    perform_oda(dataMatrix1)
