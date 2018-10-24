#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove columns which contain unusable or insufficient data.
"""

from sklearn.base import BaseEstimator, TransformerMixin  # base transformer classes
import pandas as pd


class NonNumericColumnDropper(BaseEstimator, TransformerMixin):
    """Drop columns which contain strings."""

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    @staticmethod
    def transform(x_df: pd.DataFrame):
        x_df.drop(x_df.select_dtypes(['object']), inplace=True, axis=1)
        return x_df


class ThresholdingMissingDataColumnDropper(BaseEstimator, TransformerMixin):
    """Drop columns which contain a sub threshold amount of data points."""

    def __init__(self, na_drop_threshold: int=0.5):
        self.na_drop_threshold = na_drop_threshold

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    def transform(self, x_df: pd.DataFrame):
        max_number_of_nans = self.na_drop_threshold * x_df.shape[1]
        return x_df.loc[:, (x_df.isnull().sum(axis=0) <= max_number_of_nans)]
