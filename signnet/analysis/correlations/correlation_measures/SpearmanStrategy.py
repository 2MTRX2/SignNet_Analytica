# SpearmanStrategy.py
import pandas as pd
from scipy.stats import spearmanr

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

class SpearmanStrategy(CorrelationStrategy):
    """Concrete implementation of the CorrelationStrategy using Spearman's rank correlation coefficient (Rho)."""

    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        """Calculates Spearman's rho correlation coefficient and its corresponding two-tailed p-value.

        Utilizes the SciPy stats computational engine to determine the strength and significance 
        of the rank-order association between two parallel, pre-aligned centrality data series.

        Args:
            x (pd.Series): The first variable sequence for the pairwise comparison.
            y (pd.Series): The second variable sequence, aligned element-by-element 
                with the first sequence.

        Returns:
            tuple[float, float]: A tuple containing exactly two elements:
                - The calculated Spearman correlation coefficient (rho, bounded between -1.0 and 1.0).
                - The statistical two-tailed p-value representing the significance of the monotonic association.
        """
        coeff, p_val = spearmanr(x, y)
        return float(coeff), float(p_val)