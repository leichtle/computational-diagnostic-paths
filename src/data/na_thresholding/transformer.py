from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from typing import List


class ThresholdingMissingDataColumnDropper(BaseEstimator, TransformerMixin):
    """Drop columns which contain a sub threshold amount of data points."""

    def __init__(self, na_drop_threshold: int=0.5):
        self.na_drop_threshold = na_drop_threshold

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    def transform(self, x_df: pd.DataFrame):
        nan_qty_column_drop_threshold = self.na_drop_threshold * x_df.shape[0]
        return x_df.loc[:, (x_df.isnull().sum(axis=0) <= nan_qty_column_drop_threshold)]


class ValuePresenceRowFilter(BaseEstimator, TransformerMixin):
    """Drop rows if they lack a value in a certain row."""

    def __init__(self, required_columns: List[str]=[]):
        self.required_columns = required_columns

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    def transform(self, x_df: pd.DataFrame):
        return x_df.dropna(subset=self.required_columns)
