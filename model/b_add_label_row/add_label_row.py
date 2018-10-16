#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adds a label row to the lab measurements dataset.
"""

import numpy as np
import pandas as pd
import datetime
import argparse


def add_label_row(df):
    df["I200_I2519"] = np.where(df["HDIA"].str.contains("^I([2-9][0-9][0-9]|1[0-9][0-9][0-9]|2[0-5][0-1][0-9])$"), 1, 0)  # 0,1 encode
    return df


if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Add a label row to the lab measurements dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    args = parser.parse_args()

    print("Loading dataset...")
    mi_df = pd.read_csv(args.dataset, header=0)  # read data from csv
    print("...Done.")

    print("Adding label row...")
    mi_df = add_label_row(mi_df)
    print("...Done.")

    print("Write dataset to file...")
    file_name = './b_add_label_row/results/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '-mi-imputation+label.csv'
    print(file_name)
    mi_df.to_csv(file_name, index=False)
    print("...Done.")
