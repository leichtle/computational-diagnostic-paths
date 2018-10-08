import numpy as np
import pandas as pd
import datetime


def add_label_row(df):
    df["I200_I2519"] = np.where(df["HDIA"].str.contains("^I([2-9][0-9][0-9]|1[0-9][0-9][0-9]|2[0-5][0-1][0-9])$"), 1, 0)
    return df


if __name__ == "__main__":
    mi_df = pd.read_csv('../a_imputation/results/20181003152517-mi-imputation.csv', header=0)  # read data from csv
    mi_df = add_label_row(mi_df)
    file_name = './results/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '-mi-imputation+label.csv'
    mi_df.to_csv(file_name, index=False)
