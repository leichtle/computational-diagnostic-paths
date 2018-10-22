#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prepare dataset for bayesian variable selection.
"""

import pandas as pd
import datetime
import argparse
import os
import re
import logging

from src.features.labels import add_binary_diagnosis_label
from src.features.imputations import impute

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Prepare dataset for bayesian variable selection.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--imputation_type', type=str, help='The type of imputation to perform', required=True)
    parser.add_argument('--niter', type=int, default=None, help='The number of iterations to perform, in case an interative method is chosen')

    args = parser.parse_args()
    dataset_path = args.dataset
    imputation_type = impute.ImputationType[args.imputation_type]
    iteration_qty = args.niter

    logger.info("Loading dataset...")
    mi_df = pd.read_csv(dataset_path, header=0)  # read data from csv
    logger.info("...Done.")

    logger.info("Adding binary diagnosis label...")
    mi_df = add_binary_diagnosis_label(mi_df)
    logger.info("...Done.")

    logger.info("Performing imputation")
    mi_df = impute.impute_missing_data(mi_df, imputation_type, exclude_from_imputation=["HDIA", "Klasse"], iteration_qty=iteration_qty)
    logger.info("...Done.")

    logger.info("Writing dataset to file...")
    file_name = os.path.splitext(os.path.basename(dataset_path))[0]

    # prepare dataset store path
    path = 'data/interim/'
    if not re.match("\d\d\d\d\d\d\d\d\d\d\d\d", file_name):  # try to find a timestamp with 4 digit year and each 2 digits for month, day, hour, minute, second
        path += datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_'
    path +=  file_name + '_impType_'+imputation_type.name+'_nIter_'+str(iteration_qty)+'_label.csv'
    logger.info(path)
    mi_df.to_csv(path, index=False)
    logger.info("...Done.")
