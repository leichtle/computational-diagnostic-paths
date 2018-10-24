#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Perform bayesian variable selection on dataset to calculate inclusion probabilities.
"""

import argparse

import pandas as pd

from src.models.bayesian_model_averaging.oda_probit import perform_oda_probit

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

    # load data
    mi_df = pd.read_csv(dataset_path)  # read data from csv

    label = 'I200_I2519'

    feature_names = [column_name for column_name in mi_df.colums if column_name is not label]
    # ["ALAT", "AP", "ASAT", "CA", "CK", "CREA", "CRP", "GGT", "GL", "KA", "LDH", "NA.", "TNT", "UREA"]

    # Calculate oda inclusion probabilities for ICD-10
    print("Sanity check:")
    print(mi_df.shape)
    print(mi_df.columns)

    features = mi_df[feature_names]  # extract features
    label = mi_df[label]  # extract label

    oda_results = perform_oda_probit(xo=features, zo=label, niter=iteration_qty, burn_in=burn_in_sim, lam_spec=lam_spec)

    print("Results:")
    print(oda_results["incprob_rb"])

    #print(oda_icd1["betama"])
    #print(oda_icd1["incprob"])
    #print(oda_icd1["gamma"])
    #print(oda_icd1["odds"])

