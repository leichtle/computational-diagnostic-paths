import pandas as pd
import datetime
from sklearn.preprocessing import Imputer


def selectively_impute(df):
    imputation_data = pd.DataFrame()                                            # make df for the columns to impute

    cols_with_missing = [col for col in df.columns if df[col].isnull().any()]   # find columns which require imputation

    for col in cols_with_missing:                                               # move columns to df
        imputation_data[col] = df[col]
        df.drop(columns=[col], inplace=True)

    imputer = Imputer(strategy='mean')                                          # perform imputation
    column_names = imputation_data.columns
    imputation_data = pd.DataFrame(imputer.fit_transform(imputation_data))
    imputation_data.columns = column_names

    df = pd.concat([df, imputation_data], axis=1)                               # concatenate dfs again
    return df


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
