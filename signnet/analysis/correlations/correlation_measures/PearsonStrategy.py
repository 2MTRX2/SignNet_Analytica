# PearsonStrategy.py
import pandas as pd
from scipy.stats import pearsonr

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

class PearsonStrategy(CorrelationStrategy):
    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        coeff, p_val = pearsonr(x, y)
        return float(coeff), float(p_val)