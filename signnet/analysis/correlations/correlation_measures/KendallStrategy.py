# KendallStrategy.py
import pandas as pd
from scipy.stats import kendalltau

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

class KendallStrategy(CorrelationStrategy):
    """Concrete implementation of the CorrelationStrategy using Kendall's rank correlation coefficient (Tau)."""
    
    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        """Calculates the Kendall's tau correlation coefficient and its corresponding two-tailed p-value.

        Utilizes the SciPy stats computational engine to determine the strength and significance 
        of the rank relationship between two parallel, pre-aligned centrality data series.

        Args:
            x (pd.Series): The first continuous or ordinal variable sequence for the pairwise comparison.
            y (pd.Series): The second continuous or ordinal variable sequence, aligned element-by-element 
                with the first sequence.

        Returns:
            tuple[float, float]: A tuple containing exactly two elements:
                - The calculated Kendall's tau coefficient (bounded between -1.0 and 1.0).
                - The statistical two-tailed p-value representing the significance of the rank association.
        """
        coeff, p_val = kendalltau(x, y)
        return float(coeff), float(p_val)