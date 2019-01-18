#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove rows which have no diagnosis.
"""

from sklearn.base import BaseEstimator, TransformerMixin  # base transformer classes
import pandas as pd


class MissingDiagnosisRowDropper(BaseEstimator, TransformerMixin):

    def __init__(self, diagnosis_col_name):
        self.diagnosis_col_name = diagnosis_col_name

    def fit(self, x_df: pd.DataFrame, y_df: pd.DataFrame=None):
        return self

    def transform(self, x_df: pd.DataFrame):
        x_df.dropna(axis="rows", subset=[self.diagnosis_col_name], inplace=True)
        x_df = x_df[x_df[self.diagnosis_col_name].map(lambda d: len(d)) > 0]  # keep non-zero length strings or lists
        return x_df
