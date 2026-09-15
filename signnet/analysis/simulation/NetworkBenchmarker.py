# NetworkBenchmarker.py
import pandas as pd
import numpy as np

class NetworkBenchmarker:
    """
    Responsible for benchmarking and the statistical evaluation of simulation data.
    """

    @staticmethod
    def analyze_network_extremes(df_raw_results: pd.DataFrame, node_col: str = "node") -> pd.DataFrame:
        """
        Analyses the maximum average, minimum average, and total average of the network. 

        Args:
            df_raw_results (pd.DataFrame): Unaggregated raw data from `SimulationEngine`.
                Expects the column 'iteration' at the very first position (index 0) 
                and a column for node identifiers matching `node_col`.
            node_col (str, optional): The name of the column containing the node identifiers.
                Defaults to "node".

        Returns:
            pd.DataFrame: A compact table for each centrality metric which delivers
                three global key numbers: 
                - 'metric_name': name of the analysed metric.
                - 'mean_of_maxima': average of the highest values per iteration.
                - 'mean_of_minima': average of the smallest values per iteration.
                - 'mean_of_all_values': average over all values.
        
        Raises:
            ValueError: If `df_raw_results` is None or empty.
            ValueError: If the column 'iteration' is missing.
            ValueError: If the column 'iteration' is not located at the first position (index 0).
        """
        if df_raw_results is None or df_raw_results.empty:
            raise ValueError(
                "The simulation raw data are empty and benchmarking cannot be done."
            )

        if "iteration" not in df_raw_results.columns:
            raise ValueError("Dataframe format is wrong: column 'iteration' not available.")

        
        if df_raw_results.columns[0] != "iteration":
            raise ValueError("Structural error: 'iteration' must be the very first column!")

        # 1. determining dynamically the data columns
        excluded_columns = ["iteration", node_col]
        metric_columns = [col for col in df_raw_results.columns if col not in excluded_columns]

        # 2. determining key numbers per iteration
        grouped_by_iteration = df_raw_results.groupby("iteration")[metric_columns]
        
        iteration_maxima = grouped_by_iteration.max()
        iteration_minima = grouped_by_iteration.min()
        iteration_means = grouped_by_iteration.mean()

        # 3. claculating an average over all iterations
        summary_records = []
        for metric in metric_columns:
            summary_records.append({
                "metric_name": metric,
                "mean_of_maxima": float(iteration_maxima[metric].mean()),
                "mean_of_minima": float(iteration_minima[metric].mean()),
                "mean_of_all_values": float(iteration_means[metric].mean())
            })

        return pd.DataFrame(summary_records)


    @staticmethod
    def calculate_gini_coefficient(df_raw_results: pd.DataFrame, node_col: str = "node") -> pd.DataFrame:
        """
        Calculates the average Gini-coefficient per metric.
        
        Args:
            df_raw_results (pd.DataFrame): unaggregated raw data of the engine.
            node_col (str, optional): The name of the column containing the node identifiers.
                Defaults to "node".
            
        Returns:
            pd.DataFrame: table with average Gini-coefficients per metric.

        Raises:
            ValueError: If 'df_raw_results' is 'None' or empty, it cannot do any calculations.
            ValueError: If the column 'iteration' is missing.
            ValueError: If the column 'iteration' is not located at the first position (index 0).
        """

        if df_raw_results is None or df_raw_results.empty:
            raise ValueError(
                "The simulation raw data are empty and benchmarking cannot be done."
            )

        if "iteration" not in df_raw_results.columns:
            raise ValueError("Dataframe format is wrong: column 'iteration' not available.")

        
        if df_raw_results.columns[0] != "iteration":
            raise ValueError("Structural error: 'iteration' must be the very first column!")

        excluded_columns = ["iteration", node_col]
        metric_columns = [col for col in df_raw_results.columns if col not in excluded_columns]
        
        results = []
        
        for metric in metric_columns:
            gini_per_it = []
            
            for _, df_it in df_raw_results.groupby("iteration"):
                values = df_it[metric].to_numpy(dtype=float)
                
                # Normalisation for negative centrality measures (e.g. Net-Degree)
                if np.any(values < 0): 
                    min_val = np.min(values)
                    max_val = np.max(values)
                    diff = max_val - min_val
                    values = (values - min_val) / diff if diff > 0 else np.zeros_like(values)
                
                if np.sum(values) == 0:
                    gini_per_it.append(0.0)
                    continue
                    
                # Gini algorithm
                sorted_values = np.sort(values)
                n = len(values)
                index = np.arange(1, n + 1)
                gini = (np.sum((2 * index - n - 1) * sorted_values)) / (n * np.sum(sorted_values))
                gini_per_it.append(gini)
                
            results.append({
                "metric_name": metric,
                "mean_gini_coefficient": float(np.mean(gini_per_it))
            })
            
        return pd.DataFrame(results)

