# NetworkBenchmarker.py
import pandas as pd
import numpy as np

class NetworkBenchmarker:
    """
    Responsible for benchmarking and the statistical evaluation of simulation data.
    """

    @staticmethod
    def analyze_network_extremes(df_raw_results: pd.DataFrame) -> pd.DataFrame:
        """
        Analyses the maximum average, minimum average, and total average of the network. 
        Analysiert die Maxima, Minima und Gesamtdurchschnitte des Netzwerks.

        Args:
            df_raw_results (pd.DataFrame): Unaggregated raw data from `GenericSimulationEngine`.
                Expects the columns 'iteration' and 'node'.

        Returns:
            pd.DataFrame: A companct table for each centrality metric which delivers
                three global key numbers: 
                - 'mean_of_maxima': average of the highest values per iteration.
                - 'mean_of_minima': average of the smallest values per iteration.
                - 'mean_of_all_values': average over all values.
        
        Raises:
            ValueError: If 'df_raw_results' is 'None' or empty, it cannot do any calculations.
        """
        if df_raw_results is None or df_raw_results.empty:
            raise ValueError(
                "The simulation raw data are empty and benchmarking cannot be done."
            )

        # 1. determining dynamically the data columns
        excluded_columns = ["iteration", "node"]
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
    def calculate_gini_coefficient(df_raw_results: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the average Gini-coefficient per metric.
        
        Args:
            df_raw_results (pd.DataFrame): unaggregated raw data of the engine.
            
        Returns:
            pd.DataFrame: table with average Gini-coefficients per metric.

        Raises:
            ValueError: If 'df_raw_results' is 'None' or empty, it cannot do any calculations.
        """
        if df_raw_results is None or df_raw_results.empty:
            raise ValueError(
                "The simulation raw data are empty and benchmarking cannot be done."
            )

        excluded = ["iteration", "node"]
        metric_columns = [c for c in df_raw_results.columns if c not in excluded]
        
        results = []
        
        for metric in metric_columns:
            gini_per_it = []
            
            for _, df_it in df_raw_results.groupby("iteration"):
                values = df_it[metric].to_numpy(dtype=float)
                
                # Normalisierung für negative Zentralitätswerte (z.B. Net-Degree)
                if np.any(values < 0): 
                    min_val = np.min(values)
                    max_val = np.max(values)
                    diff = max_val - min_val
                    values = (values - min_val) / diff if diff > 0 else np.zeros_like(values)
                
                if np.sum(values) == 0:
                    gini_per_it.append(0.0)
                    continue
                    
                # Mathematischer Gini-Algorithmus
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

