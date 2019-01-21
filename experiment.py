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

# xgboost
from xgboost import XGBClassifier
from xgboost import plot_importance
from matplotlib import pyplot

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Perform bayesian variable selection on dataset.')
    parser.add_argument('--dataset', type=str, help='The path to the dataset file', required=True)
    parser.add_argument('--csv_separator', type=str, help='The separator of the data columns', default=',')
    parser.add_argument('--importance_method', type=str, help='The method to determine feature importance. Options: bma=complete dataset, xgb=incomplete dataset', default='xgb')
    parser.add_argument('--niter', type=int, default=100000, help='The number of iterations to perform')
    parser.add_argument('--burn_in_sim', type=int, default=500, help='Burn in sim')
    parser.add_argument('--lam_spec', type=float, default=1, help='lam spec')
    parser.add_argument('--label', type=str, default='diagnostic_outcome', help='The name of the label column.')
    parser.add_argument('--show_plots', type=bool, help='Show plots if they are available', default=False)

    args = parser.parse_args()
    dataset_path = args.dataset
    csv_separator = args.csv_separator
    importance_method = args.importance_method
    iteration_qty = args.niter
    burn_in_sim = args.burn_in_sim
    lam_spec = args.lam_spec
    label = args.label
    show_plots = args.show_plots

    logger.info(str({"message": "NEW EXPERIMENT",
                     "path": dataset_path,
                     "iteration_qty": iteration_qty,
                     "burn_in_sim": burn_in_sim,
                     "lam_spec": lam_spec})
                )

    logger.info(str({"message": "Load dataset",
                     "path": dataset_path}))
    mi_df = pd.read_csv(dataset_path, header=0, sep=csv_separator)  # read data from csv

    logger.info("Sanity check:")
    logger.info(mi_df.shape)
    logger.info(mi_df.columns)

    if mi_df.isnull().values.any() and importance_method == 'bma':
        logger.critical(str({"messsage": "BMA can only work with a complete/imputed dataset. "
                                         "Run imputation first using dataset.py or dataset.r"}))
        exit(-1)

    # prepare data for bayesian variable selection
    feature_names = [column_name for column_name in list(mi_df) if column_name != label]  # extract feature names
    features = mi_df[feature_names]  # extract features
    labels = mi_df[label]  # extract label

    incprobs_df = pd.DataFrame(columns=feature_names)

    if importance_method == "bma":
        # Calculate oda inclusion probabilities for ICD-10
        oda_results = ODAPerformer(iteration_qty=iteration_qty, burn_in_sim=burn_in_sim, lam_spec=lam_spec).fit_transform(features, labels)

        # create a new dataset for inclusion probabilities
        incprobs_df.loc[0] = oda_results["incprob_rb"]

        logger.info(str({"message": "Results",
                         "inclusion_probabilities": incprobs_df})
                    )

        # logger.info(oda_results["betama"])
        # logger.info(oda_results["incprob"])
        # logger.info(oda_results["gamma"])
        # logger.info(oda_results["odds"])

    elif importance_method == "xgb":
        # xgradient boosting
        # source: https://machinelearningmastery.com/feature-importance-and-feature-selection-with-xgboost-in-python/
        # handling of missing values: https://stats.stackexchange.com/questions/235489/xgboost-can-handle-missing-data-in-the-forecasting-phase
        # https://stackoverflow.com/questions/37617390/xgboost-handling-of-missing-values-for-split-candidate-search

        # fit model to training data
        model = XGBClassifier()
        model.fit(features, labels)

        if show_plots:
            # plot feature importance
            plot_importance(model)
            pyplot.show()

        # create a new dataset for feature importances
        incprobs_df.loc[0] = model.feature_importances_

        logger.info(str({"message": "Results",
                         "feature_importances": incprobs_df})
                    )

        # TODO: Setup a train/test setting to validate your model

    # write dataset to file
    write_df_to_csv(df=incprobs_df, store_path='data/processed/', initial_path=dataset_path, file_appendix='_importance_method_' + importance_method + '_incprobs')

