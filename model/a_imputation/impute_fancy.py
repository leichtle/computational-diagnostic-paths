import pandas as pd
import datetime
from fancyimpute import KNN, NuclearNormMinimization, SoftImpute, IterativeImputer, BiScaler
from enum import Enum


class ImputationType(Enum):
    ITERATIVE = 0
    KNN = 1
    NNM = 2
    SOFT = 3


def impute_missing_data(df: pd.DataFrame, imputation_type: ImputationType, exclude_from_imputation=[]):

    # X is the complete data matrix
    # X_incomplete has the same values as X except a subset have been replace with NaN
    exclusion_df = df[exclude_from_imputation].copy()
    missing_data_df = df.drop(exclude_from_imputation, axis=1)
    x_incomplete = missing_data_df.values

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
    else:
        # Model each feature with missing values as a function of other features, and
        # use that estimate for imputation.
        imputed = IterativeImputer(n_iter=100000, verbose=True).fit_transform(x_incomplete)

    imputed_df = pd.DataFrame(data=imputed, columns=missing_data_df.columns, index=missing_data_df.index)
    complete_df = pd.concat([exclusion_df, imputed_df], axis=1, sort=False)
    return complete_df


if __name__ == "__main__":
    imputation_type = ImputationType.ITERATIVE
    mi_df = pd.read_csv('../../data/raw_myocardial_ischemia.csv', header=0)  # read data from csv
    mi_df = impute_missing_data(mi_df, imputation_type, exclude_from_imputation=["HDIA", "Klasse"])
    file_name = './results/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '-' + imputation_type.name + '-imputation.csv'
    mi_df.to_csv(file_name, index=False)
