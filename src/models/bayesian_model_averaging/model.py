from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

from src.models.bayesian_model_averaging.oda_probit import perform_oda_probit


class ODAPerformer(BaseEstimator, TransformerMixin):

    def __init__(self, iteration_qty, burn_in_sim, lam_spec):
        self.iteration_qty = iteration_qty
        self.burn_in_sim = burn_in_sim
        self.lam_spec = lam_spec
        self.oda_results = None

    def fit(self, x: pd.DataFrame, y: pd.DataFrame=None):
        self.oda_results = perform_oda_probit(x, y, self.iteration_qty, self.burn_in_sim, self.lam_spec)
        return self

    def transform(self, x: pd.DataFrame):
        return self.oda_results
