#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract features suitable for bayesian variable selection.
"""
import argparse
import logging

import pandas as pd
from sklearn.pipeline import Pipeline

from src.common.df_csv_writing import write_df_to_csv
from src.common.json_logging import setup_logging
from src.features.filter_columns.filter_columns import NonNumericColumnDropper
from src.features.labels.labels import BinaryLabelExtractor

setup_logging("src/common/logging.json")  # setup logger
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Extract features suitable for bayesian variable seection.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--csv_separator', type=str, help='The separator of the data columns', default=',')
    parser.add_argument('--diagnosis_code_min', type=int, default=200, help='Lowest ICD code to be considered positive diagnosis.')
    parser.add_argument('--diagnosis_code_max', type=int, default=2519, help='Highest ICD code to be considered positive diagnosis.')

    args = parser.parse_args()
    dataset_path = args.dataset
    csv_separator = args.csv_separator
    diagnosis_code_min = args.diagnosis_code_min
    diagnosis_code_max = args.diagnosis_code_max

    logger.info(str({"message": "NEW FEATURE",
                     "path": dataset_path})
                )

    logger.info(str({"message": "Load dataset",
                     "path": dataset_path}))
    mi_df = pd.read_csv(dataset_path, header=0, sep=csv_separator)  # read data from csv

    # prepare pipeline and run it
    inclusion_labels = {'I' + str(number) for number in range(diagnosis_code_min, diagnosis_code_max)}  # range of ICD10 codes for positive diagnosis
    pipeline = Pipeline([
        ('extract_label', BinaryLabelExtractor(extract_from_column='HDIA', inclusion_labels=inclusion_labels)),
        ('drop_non_numerical_columns', NonNumericColumnDropper())
    ])
    mi_df = pipeline.fit_transform(mi_df)

    # write dataset to file
    write_df_to_csv(df=mi_df, store_path='data/interim/', initial_path=dataset_path, file_appendix="_label")
