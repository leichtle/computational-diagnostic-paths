#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Impute missing values of dataset.
"""

import pandas as pd
import datetime
from fancyimpute import KNN, NuclearNormMinimization, SoftImpute, IterativeImputer, BiScaler
from enum import Enum
import argparse
import os
import re

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import Imputer
import logging

logger = logging.getLogger(__name__)


class ImputationType(Enum):
    ITERATIVE = 0
    KNN = 1
    NNM = 2
    SOFT = 3
    MEAN = 4


def impute_missing_data(df: pd.DataFrame, imputation_type: ImputationType, exclude_from_imputation: list=[], **kwargs):

    # X is the complete data matrix
    # X_incomplete has the same values as X except a subset have been replace with NaN
    if exclude_from_imputation is None:
        exclude_from_imputation = list()
    exclusion_df = df[exclude_from_imputation].copy()
    missing_data_df = df.drop(exclude_from_imputation, axis=1)
    x_incomplete = missing_data_df.values

    logger.info(str({"message":"Perform imputation of type ",
                     "imputation_tye": imputation_type.name})
                )

    if imputation_type == ImputationType.KNN:
        # Use 3 nearest rows which have a feature to fill in each row's missing features
        imputed = KNN(k=3).fit_transform(x_incomplete)
    elif imputation_type == ImputationType.NNM:
        # matrix completion using convex optimization to find low-rank solution
        # that still matches observed values. Slow!
        imputed = NuclearNormMinimization(verbose=True).fit_transform(x_incomplete)
    elif imputation_type == ImputationType.SOFT:
        # Instead of solving the nuclear norm objective directly, instead
        # induce sparsity using singular value thresholding
        x_incomplete_normalized = BiScaler().fit_transform(x_incomplete)
        imputed = SoftImpute().fit_transform(x_incomplete_normalized)
    elif imputation_type == ImputationType.MEAN:
        imputed = Imputer(strategy='mean').fit_transform(x_incomplete)  # perform imputation
    else:
        # Model each feature with missing values as a function of other features, and
        # use that estimate for imputation.
        iteration_qty = None
        if 'iteration_qty' in kwargs:
            iteration_qty = kwargs['iteration_qty']

        if iteration_qty is None:
            iteration_qty = 100000
            logging.error(str({"message": "Iteration qty not set, defaulting to " + str(iteration_qty)}))
        imputed = IterativeImputer(n_iter=iteration_qty, verbose=True).fit_transform(x_incomplete)

    imputed_df = pd.DataFrame(data=imputed, columns=missing_data_df.columns, index=missing_data_df.index)
    complete_df = pd.concat([exclusion_df, imputed_df], axis=1, sort=False)
    return complete_df


class DataImputer(BaseEstimator, TransformerMixin):

    def __init__(self, imputation_type: ImputationType, exclude_from_imputation: list=[], **kwargs):
        self.imputation_type = imputation_type
        self.exclude_from_imputation = exclude_from_imputation
        self.kwargs = kwargs

    def fit(self, x: pd.DataFrame, y: pd.DataFrame=None):
        return self

    def transform(self, x: pd.DataFrame):
        df = impute_missing_data(x, imputation_type=self.imputation_type, exclude_from_imputation=self.exclude_from_imputation, **self.kwargs)
        return df


if __name__ == "__main__":
    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Impute missing values of dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--imputation_type', type=str, help='The type of imputation to perform', required=True)
    parser.add_argument('--niter', type=int, default=100000, help='The number of iterations to perform, in case an interative method is chosen')
    args = parser.parse_args()
    dataset_path = args.dataset
    imputation_type = ImputationType[args.imputation_type]
    iteration_qty = args.niter

    # load dataset
    mi_df = pd.read_csv('../../data/raw_myocardial_ischemia.csv', header=0)  # read data from csv
    mi_df = impute_missing_data(mi_df, imputation_type, exclude_from_imputation=["HDIA", "Klasse"], iteration_qty=iteration_qty)

    file_name = os.path.splitext(os.path.basename(dataset_path))[0]

    if re.match("\d\d\d\d\d\d\d\d\d\d\d\d", file_name):  # is no timestamp present? (with 4 digit year and each 2 digits for month, day, hour, minute, second)
        path = 'data/interim/' + file_name + '-imputation.csv'
    else:
        path = 'data/interim/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + file_name + '-imputation.csv'
    print(path)

    file_name = './results/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '-' + imputation_type.name + '-imputation.csv'
    mi_df.to_csv(file_name, index=False)
