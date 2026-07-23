# SpearmanStrategy.py
import pandas as pd
from scipy.stats import spearmanr

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

class SpearmanStrategy(CorrelationStrategy):
    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        coeff, p_val = spearmanr(x, y)
        return float(coeff), float(p_val)