#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove rows which are zero sum.
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin  # base transformer classes


class ZeroSumDropper(BaseEstimator, TransformerMixin):
    """Drop columns which contain strings."""

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    @staticmethod
    def transform(x_df: pd.DataFrame):
        print(len(x_df))
        x_df = x_df[(x_df > 0 | x_df.isna()).all(1)]
        print(len(x_df))
        return x_df
