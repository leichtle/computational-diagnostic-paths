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
        x_df.drop(x_df.select_dtypes(['bool']), inplace=True, axis=1)
        return x_df

