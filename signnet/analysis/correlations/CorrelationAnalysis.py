import pandas as pd
import numpy as np

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy 

class CorrelationAnalysis: 

    def __init__(self, strategy: CorrelationStrategy):
        self.strategy = strategy

    def analyze_correlations(self, centrality_measures: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        df = centrality_measures.copy()

        possible_node_names = ['node', 'node_id', 'id']
        for col in df.columns:
            if str(col).lower() in possible_node_names:
                df = df.set_index(col)
                break

        df = df.select_dtypes(include=[np.number])

        columns = df.columns
        n_cols = len(columns)
        
        corr_matrix = np.zeros((n_cols, n_cols))
        p_matrix = np.zeros((n_cols, n_cols))

        for i in range(n_cols):
            for j in range(n_cols):
                if i == j:
                    corr_matrix[i, j] = 1.0
                    p_matrix[i, j] = 0.0
                else:
                    valid_data = centrality_measures[[columns[i], columns[j]]].dropna()
                    
                    if len(valid_data) > 1:
                        # Hier rufen wir polymorph die Berechnung der gewählten Strategie auf
                        coeff, p_val = self.strategy.calculate(valid_data[columns[i]], valid_data[columns[j]])
                        corr_matrix[i, j] = coeff
                        p_matrix[i, j] = p_val
                    else:
                        corr_matrix[i, j] = np.nan
                        p_matrix[i, j] = np.nan

        corr_df = pd.DataFrame(corr_matrix, index=columns, columns=columns)
        p_values_df = pd.DataFrame(p_matrix, index=columns, columns=columns)
        
        return corr_df, p_values_df
