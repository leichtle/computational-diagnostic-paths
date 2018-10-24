#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Perform bayesian variable selection to obtain inclusion probabilities.
"""

import argparse
import logging

import pandas as pd

from src.common.df_csv_writing import write_df_to_csv
from src.models.bayesian_model_averaging.model import ODAPerformer

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Perform bayesian variable selection on dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--niter', type=int, default=100000, help='The number of iterations to perform')
    parser.add_argument('--burn_in_sim', type=int, default=500, help='Burn in sim')
    parser.add_argument('--lam_spec', type=float, default=1, help='lam spec')
    args = parser.parse_args()
    dataset_path = args.dataset
    iteration_qty = args.niter
    burn_in_sim = args.burn_in_sim
    lam_spec = args.lam_spec

    logger.info(str({"message": "NEW EXPERIMENT",
                     "path": dataset_path,
                     "na_drop_threshold": iteration_qty,
                     "burn_in_sim": burn_in_sim,
                     "lam_spec": lam_spec})
                )

    logger.info(str({"message": "Load dataset",
                     "path": dataset_path}))
    mi_df = pd.read_csv(dataset_path, header=0)  # read data from csv

    logger.info("Sanity check:")
    logger.info(mi_df.shape)
    logger.info(mi_df.columns)

    # prepare data for bayesian variable selection
    label = 'diagnostic_outcome'  # declare label
    feature_names = [column_name for column_name in list(mi_df) if column_name is not label]  # extract feature names
    features = mi_df[feature_names]  # extract features
    labels = mi_df[label]  # extract label

    # Calculate oda inclusion probabilities for ICD-10
    oda_results = ODAPerformer(iteration_qty=iteration_qty, burn_in_sim=burn_in_sim, lam_spec=lam_spec).fit_transform(features, labels)

    # create a new dataset for inclusion probabilities
    incprobs_df = pd.DataFrame(columns=feature_names)
    incprobs_df.loc[0] = oda_results["incprob_rb"]

    logger.info(str({"message": "Results",
                     "inclusion_probabilities": incprobs_df})
                )

    # logger.info(oda_results["betama"])
    # logger.info(oda_results["incprob"])
    # logger.info(oda_results["gamma"])
    # logger.info(oda_results["odds"])

    # write dataset to file
    write_df_to_csv(df=incprobs_df, store_path='data/interim/', initial_path=dataset_path, file_appendix='_incprobs')

