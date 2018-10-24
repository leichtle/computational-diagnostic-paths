#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prepare dataset for bayesian variable selection.
"""

import argparse
import logging

import pandas as pd
from sklearn.pipeline import Pipeline

from src.common.df_csv_writing import write_df_to_csv
from src.common.json_logging import setup_logging
from src.data.imputations import impute
from src.data.imputations.impute import DataImputer
from src.data.na_thresholding.transformer import ThresholdingMissingDataColumnDropper

setup_logging("src/common/logging.json")  # setup logger
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Prepare dataset for bayesian variable selection.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--csv_separator', type=str, help='The separator of the data columns', default=',')
    parser.add_argument('--na_drop_threshold', type=float, default=0.5, help='Amount of NA in column for it to be dropped [0;1]')
    parser.add_argument('--imputation_type', type=str, help='The type of imputation to perform', required=True)
    parser.add_argument('--niter', type=int, default=None, help='The number of iterations to perform, in case an interative method is chosen')

    args = parser.parse_args()
    dataset_path = args.dataset
    csv_separator = args.csv_separator
    na_drop_threshold = args.na_drop_threshold
    imputation_type = impute.ImputationType[args.imputation_type]
    iteration_qty = args.niter

    logger.info(str({"message": "NEW DATASET",
                     "path": dataset_path,
                     "imputation_type": imputation_type,
                     "iteration_qty": iteration_qty})
                )

    file_appendix = ''  # prepare file appendix telling us what has been done

    logger.info(str({"message": "Load dataset",
                     "path": dataset_path}))
    mi_df = pd.read_csv(dataset_path, header=0, sep=csv_separator)  # read data from csv

    # prepare pipeline and run it
    pipeline = Pipeline([
        ('drop_above_threshold_na_columns', ThresholdingMissingDataColumnDropper(na_drop_threshold=na_drop_threshold)),
        ('impute_missing_values', DataImputer(imputation_type=imputation_type, iteration_qty=iteration_qty))
    ])
    mi_df = pipeline.fit_transform(mi_df)
    file_appendix += '_naDropThreshold_' + str(na_drop_threshold)
    file_appendix += '_impType_' + imputation_type.name + '_nIter_' + str(iteration_qty)

    # write dataset to file
    write_df_to_csv(df=mi_df, store_path='data/interim/', initial_path=dataset_path, file_appendix=file_appendix)
