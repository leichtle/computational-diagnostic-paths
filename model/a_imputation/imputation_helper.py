import pandas as pd
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
