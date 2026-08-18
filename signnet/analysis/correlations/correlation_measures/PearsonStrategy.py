# PearsonStrategy.py
import pandas as pd
from scipy.stats import pearsonr

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

class PearsonStrategy(CorrelationStrategy):
    """Concrete implementation of the CorrelationStrategy using Pearson's product-moment correlation coefficient.    """

    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        """
        Calculates Pearson's r correlation coefficient and its corresponding two-tailed p-value.

        Utilizes the SciPy stats computational engine to determine the strength and significance 
        of the linear association between two parallel, pre-aligned centrality data series.

        Args:
            x (pd.Series): The first continuous variable sequence for the pairwise comparison.
            y (pd.Series): The second continuous variable sequence, aligned element-by-element 
                with the first sequence.

        Returns:
            tuple[float, float]: A tuple containing exactly two elements:
                - The calculated Pearson correlation coefficient (r, bounded between -1.0 and 1.0).
                - The statistical two-tailed p-value representing the significance of the linear association.
        """
        coeff, p_val = pearsonr(x, y)
        return float(coeff), float(p_val)