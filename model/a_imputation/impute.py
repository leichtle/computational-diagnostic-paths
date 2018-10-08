import pandas as pd
from model.a_imputation.imputation_helper import selectively_impute
import datetime


def impute_missing_data(df):

    print("Performing imputation...")
    df = selectively_impute(df)  # perform selective imputation
    print("...Done.")

    print("----------------------")
    print("Imputed data for inspection:")
    print(df.head())                 # print data for sanity check

    return df


if __name__ == "__main__":
    mi_df = pd.read_csv('../../data/raw_myocardial_ischemia.csv', header=0)  # read data from csv
    mi_df = impute_missing_data(mi_df)
    file_name = './results/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '-mi-imputation.csv'
    mi_df.to_csv(file_name, index=False)
