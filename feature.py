#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract features suitable for bayesian variable selection.
"""
import argparse
import ast
import logging

import pandas as pd
from sklearn.pipeline import Pipeline

from src.common.df_csv_writing import write_df_to_csv
from src.common.json_logging import setup_logging
from src.features.diagnoses.diagnoses import MissingDiagnosisRowDropper
from src.features.filter.filter_columns import NonNumericColumnDropper
from src.features.labels.labels import BinaryLabelExtractor

setup_logging("src/common/logging.json")  # setup logger
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Extract features suitable for bayesian variable seection.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--csv_separator', type=str, help='The separator of the data columns', default=',')
    parser.add_argument('--diagnosis_col_name', type=str, default='HDIA', help='The name of the diagnosis column in the data frame.')
    parser.add_argument('--diagnosis_code_min', type=int, default=200, help='Lowest ICD-10 code to be considered positive diagnosis.')
    parser.add_argument('--diagnosis_code_max', type=int, default=259, help='Highest ICD-10 code to be considered positive diagnosis.')
    parser.add_argument('--single-diagnosis', type=bool, default=False, help="If the diagnosis field contains a single diagnosis or a list.")

    args = parser.parse_args()
    dataset_path = args.dataset
    csv_separator = args.csv_separator
    diagnosis_col_name = args.diagnosis_col_name
    diagnosis_code_min = args.diagnosis_code_min
    diagnosis_code_max = args.diagnosis_code_max
    single_diagnosis = args.single_diagnosis

    logger.info(str({"message": "NEW FEATURE",
                     "path": dataset_path}))

    logger.info(str({"message": "Load dataset",
                     "path": dataset_path}))
    if single_diagnosis:
        df = pd.read_csv(dataset_path, header=0, sep=csv_separator)  # read data from csv
    else:
        df = pd.read_csv(dataset_path, header=0, sep=csv_separator, converters={diagnosis_col_name: ast.literal_eval})  # read data from csv


    # prepare pipeline and run it
    inclusion_labels = {'I' + str(number) for number in range(diagnosis_code_min, diagnosis_code_max)}  # range of ICD10 codes for positive diagnosis
    pipeline = Pipeline([
        ('drop_rows_without_diagnosis', MissingDiagnosisRowDropper(diagnosis_col_name=diagnosis_col_name)),
        ('extract_binary_label_from_diagnoses', BinaryLabelExtractor(extract_from_column=diagnosis_col_name, inclusion_labels=inclusion_labels)),
        ('drop_non_numerical_columns', NonNumericColumnDropper())
    ])
    df = pipeline.fit_transform(df)

    # write dataset to file
    write_df_to_csv(df=df, store_path='data/processed/', initial_path=dataset_path, file_appendix="_label")
