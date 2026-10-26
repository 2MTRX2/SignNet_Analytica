# test_NetworkBenchmarker
import pytest
import pandas as pd
import numpy as np

from signnet.analysis.simulation.NetworkBenchmarker import NetworkBenchmarker


@pytest.fixture
def sample_simulation_data():
    """Provides a valid, multi-metric raw simulation DataFrame for benchmarking tests."""
    data = {
        "iteration":[0, 0, 0, 1, 1, 1],
        "node":[0, 1, 2, 0, 1, 2],
        "degree": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],  # Iteration 0: min=1, max=3 | Iteration 1: min=4, max=6
        "betweenness": [0.0, 0.5, 1.0, 0.2, 0.4, 0.6]
    }
    return pd.DataFrame(data)


class TestNetworkBenchmarkerValidation:
    """Tests the input validation logic shared across both static benchmarking methods."""

    @pytest.mark.parametrize("method", [
        NetworkBenchmarker.analyze_network_extremes,
        NetworkBenchmarker.calculate_gini_coefficient
    ])
    def test_raises_value_error_for_none_or_empty_dataframe(self, method):
        # Assert handling of None input
        with pytest.raises(ValueError, match="simulation raw data are empty"):
            method(df_raw_results=None)
            
        # Assert handling of empty DataFrame input
        with pytest.raises(ValueError, match="simulation raw data are empty"):
            method(df_raw_results=pd.DataFrame())

    @pytest.mark.parametrize("method", [
        NetworkBenchmarker.analyze_network_extremes,
        NetworkBenchmarker.calculate_gini_coefficient
    ])
    def test_raises_value_error_for_missing_iteration_column(self, method):
        # Create an invalid DataFrame without the 'iteration' column
        invalid_df = pd.DataFrame({"node":[0,1], "metric": [0.5, 0.6]})
        
        with pytest.raises(ValueError, match="column 'iteration' not available"):
            method(df_raw_results=invalid_df)

    @pytest.mark.parametrize("method", [
        NetworkBenchmarker.analyze_network_extremes,
        NetworkBenchmarker.calculate_gini_coefficient
    ])
    def test_raises_value_error_for_missing_node_column(self, method):
        # Arrange: Create a dataframe where 'node' is missing but 'iteration' is there
        invalid_df = pd.DataFrame({"iteration":[0, 0], "metric": [0.5, 0.6]})
        
        # Act & Assert
        with pytest.raises(ValueError, match="column 'node' not available"):
            method(df_raw_results=invalid_df, node_col="node")


class TestNetworkBenchmarkerExtremes:
    """Tests the statistical aggregation logic of the analyze_network_extremes method."""

    def test_analyze_network_extremes_success(self, sample_simulation_data):
        # Act
        result_df = NetworkBenchmarker.analyze_network_extremes(
            df_raw_results=sample_simulation_data, 
            node_col="node"
        )

        # Assert: General structure verification
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 2  # Two metrics: 'degree' and 'betweenness'
        assert list(result_df.columns) == ["metric_name", "mean_of_maxima", "mean_of_minima", "mean_of_all_values"]

        # Assert: Mathematical verification for 'degree' metric
        # Iteration 0: max=3, min=1, mean=2
        # Iteration 1: max=6, min=4, mean=5
        # Expected means over both iterations: max=(3+6)/2=4.5 | min=(1+4)/2=2.5 | all=(2+5)/2=3.5
        degree_row = result_df[result_df["metric_name"] == "degree"].iloc[0]
        assert degree_row["mean_of_maxima"] == 4.5
        assert degree_row["mean_of_minima"] == 2.5
        assert degree_row["mean_of_all_values"] == 3.5

    def test_analyze_network_extremes_with_custom_node_column_name(self, sample_simulation_data):
        # Arrange: Rename node column to test flexibility
        custom_df = sample_simulation_data.rename(columns={"node": "custom_node_id"})

        # Act
        result_df = NetworkBenchmarker.analyze_network_extremes(
            df_raw_results=custom_df, 
            node_col="custom_node_id"
        )

        # Assert: Ensure it correctly skips 'custom_node_id' and processes the metrics
        assert len(result_df) == 2
        assert "degree" in result_df["metric_name"].values


class TestNetworkBenchmarkerGini:
    """Tests the Gini coefficient calculations including standard, zero, and negative edge cases."""

    def test_calculate_gini_coefficient_standard_values(self):
        # Arrange: Setup an iteration with unequal distribution to yield a predictable Gini coefficient
        data = {
            "iteration": [0, 0, 0],
            "node": [0, 1, 2],
            "metric": [1.0, 3.0, 6.0]  # Sorted values: 1, 3, 6
        }
        df = pd.DataFrame(data)
        
        # Act
        result_df = NetworkBenchmarker.calculate_gini_coefficient(df_raw_results=df, node_col="node")
        
        # Assert
        gini_val = result_df[result_df["metric_name"] == "metric"].iloc[0]["mean_gini_coefficient"]
        # Expected manual calculation for Gini of:
        # n = 3, sum = 10. index = [1, 2, 3]
        # num = (2*1 - 4)*1 + (2*2 - 4)*3 + (2*3 - 4)*6 = (-2)*1 + (0)*3 + (2)*6 = 10
        # Gini = 10 / (3 * 10) = 0.333333...
        assert pytest.approx(gini_val, rel=1e-5) == 0.333333

    def test_calculate_gini_coefficient_all_zeros_returns_zero(self):
        # Arrange: Setup data where all metric values are zero
        data = {
            "iteration": [0, 0],
            "node": [0, 1],
            "metric": [0.0, 0.0]
        }
        df = pd.DataFrame(data)

        # Act
        result_df = NetworkBenchmarker.calculate_gini_coefficient(df_raw_results=df)

        # Assert: Gini coefficient should gracefully handle division-by-zero bounds and return 0.0
        gini_val = result_df.iloc[0]["mean_gini_coefficient"]
        assert gini_val == 0.0

    def test_calculate_gini_coefficient_handles_negative_values_via_min_max_scaling(self):
        # Arrange: Setup data with negative entries (e.g. Net-Degree metrics)
        data = {
            "iteration": [0, 0, 0],
            "node": [0, 1, 2],
            "metric": [-10.0, 0.0, 10.0]
        }
        df = pd.DataFrame(data)
        # Min-max scaling will scale [-10, 0, 10] into [0.0, 0.5, 1.0]
        # Gini of [0, 0.5, 1] -> sum=1.5, n=3.
        # num = (2*1 - 4)*0 + (2*2 - 4)*0.5 + (2*3 - 4)*1 = 0 + 0 + 2 = 2
        # Gini = 2 / (3 * 1.5) = 2 / 4.5 = 0.444444...

        # Act
        result_df = NetworkBenchmarker.calculate_gini_coefficient(df_raw_results=df)

        # Assert
        gini_val = result_df.iloc[0]["mean_gini_coefficient"]
        assert pytest.approx(gini_val, rel=1e-5) == 0.444444
