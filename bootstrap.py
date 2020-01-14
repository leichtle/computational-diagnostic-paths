#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Perform bootstrapping to get median and confidence intervals, then visualize medians and confidence intervals as barplot and boxplot in pandas
"""

import argparse
import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from numpy import median

logger = logging.getLogger(__name__)

top_n_analytes = 20

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Perform bayesian variable selection on dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True, action='append')
    parser.add_argument('--csv_separator', type=str, help='The separator of the data columns', default=',')

    args = parser.parse_args()
    dataset_paths = args.dataset
    csv_separator = args.csv_separator

    logger.info(str({"message": "NEW VISUALIZATION",
                     "datasets": dataset_paths})
                )

    logger.info(str({"message": "Load datasets",
                     "paths": dataset_paths}))

    # load separate bayesian variable inclusion probabilities
    dfs = []
    for path in dataset_paths:
        df = pd.read_csv(path, sep=csv_separator)
        dfs.append(df)  # read data from csv

    # concatenate the calculated inclusion probabilities
    master_df = pd.concat(dfs)

    # order columns by the median
    master_df = master_df.reindex(master_df.median(axis=0).sort_values(ascending=False).index, axis=1)

    print("Top N analytes")
    print(list(master_df.columns)[:top_n_analytes])

    # keep only the top-n columns
    master_df = master_df.drop(labels=list(master_df.columns)[top_n_analytes:], axis=1)

    # use index as the ODA/BMA iteration number
    master_df.reset_index(inplace=True)
    master_df['iteration'] = master_df.index

    # prepare columns to melt down into the 'variable' column
    value_columns = list(master_df.columns)
    value_columns.remove('iteration')
    value_columns.remove('index')

    # melt value vars into the 'variable' column
    melt_df = pd.melt(master_df, id_vars=['iteration'], value_vars=value_columns)

    # visualize top-n analytes median and confidence intervals
    sns.set(style='whitegrid')
    ax = sns.barplot(x="variable", y="value", data=melt_df, estimator=median, ci=95, n_boot=1000)
    plt.title("Analyte Inclusion Probabilities")
    plt.xlabel("Analyte")
    plt.ylabel("Inclusion probability (Median, CI 95%)")
    plt.xticks(rotation=-45, ha='left')
    plt.subplots_adjust(bottom=0.2)  # or whatever
    plt.show()
