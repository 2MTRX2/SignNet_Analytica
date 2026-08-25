# CorrelationAnalysis.py
import pandas as pd
import numpy as np
from typing import Optional, Iterable

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy 

class CorrelationAnalysis: 
    """
    Executes multi-metric statistical correlation analyses over computed network centrality measures.

    This class coordinates the workflow for evaluating relationships between different centrality 
    metrics. It cleans input data, standardizes row indexing, strips non-numeric columns, and 
    delegates individual pairwise statistical calculations to an injected concrete implementation 
    of the CorrelationStrategy behavioral pattern.
    """

    def __init__(self, strategy: CorrelationStrategy):
        """
        Initializes the analysis class with a specific statistical correlation strategy.

        Args:
            strategy (CorrelationStrategy): An instantiated strategy object (e.g., Pearson, 
                Spearman) that determines the mathematical algorithm used for pairwise evaluation.
        """
        self.strategy = strategy

    def analyze_correlations(self, 
                             centrality_measures: pd.DataFrame,
                             candidate_index_columns: Optional[Iterable[str]] = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Calculates square matrices for correlation coefficients and corresponding p-values.

        Processes the input metrics table by dynamically resolving the node identifier column and 
        filtering out text attributes. It initializes empty matrices and performs an all-pairs 
        iteration loop. For each distinct metric pair, it drops rows containing structural missing 
        values (NaNs), verifies sample density, and triggers the active calculation strategy.

        Args:
            centrality_measures (pd.DataFrame): A DataFrame where columns represent individual 
                centrality metrics and rows represent network nodes.
            candidate_index_columns (Optional[Iterable[str]], optional): An iterable collection of 
                potential column labels to search and assign as the unique node identifier index. 
                If None, defaults to ['node', 'node_id', 'id']. Defaults to None.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: A tuple containing exactly two square DataFrames:
                - The first DataFrame maps pairwise correlation coefficients (-1.0 to 1.0).
                - The second DataFrame maps corresponding statistical significance p-values.
        """
        df = centrality_measures.copy()

        # search and define the row index of the centrality measures
        if candidate_index_columns is None:
            candidate_index_columns = ["node", "node_id", "id"]

        search_set = {str(name).lower() for name in candidate_index_columns}

        for col in df.columns:
            if str(col).lower() in search_set:
                df = df.set_index(col)
                break

        # select only numbers as valid datatype
        df = df.select_dtypes(include=[np.number])

        columns = df.columns
        n_cols = len(columns)

        # create a matrix which has the size of the number of centrality measures and fill it with 0s
        corr_matrix = np.zeros((n_cols, n_cols))
        p_matrix = np.zeros((n_cols, n_cols))

        # fill out the diagonal with 1.0 and add each correlation value to the matrix
        for i in range(n_cols):
            for j in range(n_cols):
                if i == j:
                    corr_matrix[i, j] = 1.0
                    p_matrix[i, j] = 0.0
                else:
                    valid_data = df[[columns[i], columns[j]]].dropna()
                    
                    if len(valid_data) > 1:
                        # invoke of the calculation of the appropriate correlation strategy
                        coeff, p_val = self.strategy.calculate(valid_data[columns[i]], valid_data[columns[j]])
                        corr_matrix[i, j] = coeff
                        p_matrix[i, j] = p_val
                    else:
                        corr_matrix[i, j] = np.nan
                        p_matrix[i, j] = np.nan

        corr_df = pd.DataFrame(corr_matrix, index=columns, columns=columns)
        p_values_df = pd.DataFrame(p_matrix, index=columns, columns=columns)
        
        return corr_df, p_values_df
