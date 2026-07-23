# KendallStrategy.py
import pandas as pd
from scipy.stats import kendalltau

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

class KendallStrategy(CorrelationStrategy):
    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        coeff, p_val = kendalltau(x, y)
        return float(coeff), float(p_val)