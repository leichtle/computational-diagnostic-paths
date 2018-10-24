from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class ThresholdingMissingDataColumnDropper(BaseEstimator, TransformerMixin):
    """Drop columns which contain a sub threshold amount of data points."""

    def __init__(self, na_drop_threshold: int=0.5):
        self.na_drop_threshold = na_drop_threshold

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    def transform(self, x_df: pd.DataFrame):
        max_number_of_nans = self.na_drop_threshold * x_df.shape[0]
        return x_df.loc[:, (x_df.isnull().sum(axis=0) <= max_number_of_nans)]
