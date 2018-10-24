#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adds a label row to the lab measurements dataset.
"""
import argparse
import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from src.common.df_csv_writing import write_df_to_csv

logger = logging.getLogger(__name__)


class BinaryLabelExtractor(BaseEstimator, TransformerMixin):
    """Extract binary label from other columns."""

    def __init__(self, extract_from_column: str='', extract_to_column: str='diagnostic_outcome', inclusion_labels: set={}):
        self.extract_from_column = extract_from_column
        self.extract_to_column = extract_to_column
        self.inclusion_labels = inclusion_labels

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    def transform(self, x_df: pd.DataFrame):
        x_df[self.extract_to_column] = np.where(x_df[self.extract_from_column].isin(self.inclusion_labels), 1, 0)  # 0,1 encode diagnosis
        return x_df


if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Add a label row to the lab measurements dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    args = parser.parse_args()
    dataset_path = args.dataset

    logger.info("Loading dataset...")
    mi_df = pd.read_csv(dataset_path, header=0)  # read data from csv

    logger.info("Adding label row...")
    inclusion_labels = {'I' + str(number) for number in range(200, 2519)}
    mi_df = BinaryLabelExtractor(extract_from_column='MainDiagnosis', inclusion_labels=inclusion_labels).fit_transform(mi_df)

    # write dataset to file
    write_df_to_csv(df=mi_df, store_path='data/interim/', initial_path=dataset_path, file_appendix='_label')

