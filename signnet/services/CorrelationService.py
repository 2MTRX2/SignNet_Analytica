# CorrelationService.py
import pandas as pd
from typing import Tuple

from signnet.analysis.correlations.CorrelationAnalysis import CorrelationAnalysis

class CorrelationService:
    """
    Executes advanced statistical correlation analysis and hypothesis testing across network metrics.
    """
    def __init__(self):
        pass

    def compute_correlations(
        self, 
        centrality_df: pd.DataFrame, 
        strategy_instance
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Computes statistical correlation coefficients and corresponding p-value matrices.

        Args:
            centrality_df (pd.DataFrame): The consolidated data matrix containing calculated centrality 
                measures across network nodes, where columns represent individual metrics.
            strategy_instance (object): An instantiated strategy class mapping to the user's selected 
                correlation metric algorithm.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two symmetric matrices:
                - df_corr: Calculated correlation coefficients bounded between -1.0 and 1.0.
                - df_p_values: Calculated two-tailed probability values (p-values) representing 
                  statistical significance.

        Raises:
            ValueError: If mathematical constraints or alignment errors are encountered during computation.
        """
        # Use Pipeline Class
        analyzer = CorrelationAnalysis(strategy=strategy_instance)
        
        # Execution & Calculation
        df_corr, df_p_values = analyzer.analyze_correlations(centrality_df)
        
        return df_corr, df_p_values
