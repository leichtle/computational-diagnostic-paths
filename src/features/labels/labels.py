#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adds a label row to the lab measurements dataset.
"""

import numpy as np
import pandas as pd
import datetime
import argparse
import os
import re


def add_binary_diagnosis_label(df: pd.DataFrame):
    df["I200_I2519"] = np.where(df["HDIA"].str.contains("^I[2-9][0-9][0-9]|1[0-9][0-9][0-9]|2[0-5][0-1][0-9]$"), 1, 0)  # 0,1 encode diagnosis of myocardial ischemia
    return df


if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Add a label row to the lab measurements dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    args = parser.parse_args()
    dataset_path = args.dataset

    print("Loading dataset...")
    mi_df = pd.read_csv(dataset_path, header=0)  # read data from csv
    print("...Done.")

    print("Adding label row...")
    mi_df = add_binary_diagnosis_label(mi_df)
    print("...Done.")

    print("Write dataset to file...")
    file_name = os.path.splitext(os.path.basename(dataset_path))[0]

    if re.match("\d\d\d\d\d\d\d\d\d\d\d\d", file_name):  # try to find a timestamp with 4 digit year and each 2 digits for month, day, hour, minute, second
        path = 'data/interim/' + file_name + '+label.csv'
    else:
        path = 'data/interim/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + file_name + '+label.csv'
    print(path)
    mi_df.to_csv(path, index=False)
    print("...Done.")
