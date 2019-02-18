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
from src.data.na_thresholding.transformer import ThresholdingMissingDataColumnDropper, ValuePresenceRowFilter

setup_logging("src/common/logging.json")  # setup logger
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Prepare dataset for bayesian variable selection.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--csv_separator', type=str, default=',', help='The separator of the data columns')
    parser.add_argument('--diagnosis_indicator_column', action='append', help='Typical measurements done when evaluating the plausibility of a certain diagnosis. Repeat flag to provide multiple columns')
    parser.add_argument('--skip_na_drop_threshold', action='store_true', help='Skip drop thresholding')
    parser.add_argument('--na_drop_threshold', type=float, default=1.0, help='Minimum amount of NA in column for it to be dropped [0;1]')
    parser.add_argument('--skip_imputation', action='store_true', help='Skip imputation')
    parser.add_argument('--imputation_type', type=str, default='ITERATIVE', help='The type of imputation to perform')
    parser.add_argument('--niter', type=int, default=1000, help='The number of iterations to perform, in case an interative method is chosen')

    args = parser.parse_args()
    dataset_path = args.dataset
    csv_separator = args.csv_separator
    indicator_columns = args.diagnosis_indicator_column
    do_na_drop_threshold = not args.skip_na_drop_threshold
    na_drop_threshold = args.na_drop_threshold
    do_imputation = not args.skip_imputation
    imputation_type = impute.ImputationType[args.imputation_type]
    iteration_qty = args.niter

    logger.info(str({"message": "PREPARE NEW DATASET",
                     "path": dataset_path,
                     "imputation_type": imputation_type,
                     "iteration_qty": iteration_qty})
                )

    file_appendix = ''  # prepare file appendix telling us what has been done

    logger.info(str({"message": "Load dataset",
                     "path": dataset_path}))
    df = pd.read_csv(dataset_path, header=0, sep=csv_separator)  # read data from csv

    # prepare pipeline and run it
    components = []
    if indicator_columns is not [] and indicator_columns is not None:
        components.append(('filter_by_indicator_columns', ValuePresenceRowFilter(required_columns=indicator_columns)))
    file_appendix += '_indicatorCols_' + str(indicator_columns)

    if do_na_drop_threshold:
        components.append(('drop_above_threshold_na_columns', ThresholdingMissingDataColumnDropper(na_drop_threshold=na_drop_threshold)))
        file_appendix += '_naLimit_' + str(na_drop_threshold)

    if do_imputation:
        components.append(('impute_missing_values', DataImputer(imputation_type=imputation_type, iteration_qty=iteration_qty)))
        file_appendix += '_impType_' + imputation_type.name + '_nIter_' + str(iteration_qty)

    pipeline = Pipeline(components)
    df = pipeline.fit_transform(df)  # apply pipeline

    logger.info({"message": "Results",
                 "dataset dimensions":
                 df.shape})

    # write dataset to file
    write_df_to_csv(df=df, store_path='data/interim/', initial_path=dataset_path, file_appendix=file_appendix)
