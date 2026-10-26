# test_SimulationEngine.py
import pytest
import pandas as pd
from unittest.mock import MagicMock, mock_open

from signnet.analysis.simulation.SimulationEngine import SimulationEngine
from signnet.models.SignedNetwork import SignedNetwork


@pytest.fixture
def mock_analysis_pipeline():
    """Provides a dummy analysis pipeline returning a sample DataFrame."""
    def dummy_pipeline(network: SignedNetwork) -> pd.DataFrame:
        # Create a mock metrics DataFrame where the index represents node IDs
        data = {"metric_val": [0.8, 0.2, 0.5]}
        df = pd.DataFrame(data, index=[10, 20, 30])
        df.index.name = "node_id"
        return df
        
    return dummy_pipeline


class TestSimulationEngine:
    """Tests covering the execution and normalization logic of SimulationEngine."""

    def test_run_with_callable_generator(self, mock_analysis_pipeline):
        # Arrange
        engine = SimulationEngine(analysis_pipeline=mock_analysis_pipeline)
        
        # Create a mock callable network generator that counts invocations
        mock_network_generator = MagicMock()
        mock_signed_network = MagicMock(spec=SignedNetwork)
        mock_network_generator.return_value = mock_signed_network

        # Act: Run simulation for 3 iterations using the generator function
        result_df = engine.run(num_iterations=3, network_provider=mock_network_generator)

        # Assert: Verify the generator was called exactly once per iteration
        assert mock_network_generator.call_count == 3
        
        # Assert: Validate the shape and contents of the unified final DataFrame
        # 3 iterations * 3 nodes per iteration = 9 rows total
        assert len(result_df) == 9
        assert list(result_df.columns) == ["iteration", "node_id", "metric_val"]
        
        # Verify iteration counter sequence across the consolidated dataframe
        expected_iterations = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        assert list(result_df["iteration"]) == expected_iterations

    def test_run_with_static_object_triggers_copy(self, mock_analysis_pipeline):
        # Arrange
        engine = SimulationEngine(analysis_pipeline=mock_analysis_pipeline)
        
        # We build a tiny, real class stub that behaves exactly like your SignedNetwork object
        class StubSignedNetwork:
            def __init__(self):
                self.copy_count = 0
                
            def copy(self):
                self.copy_count += 1
                return self # Returns itself, which is sufficient for this test

        # Instantiate our stub (it is NOT a callable, so the Engine's if-statement will trigger)
        stub_network = StubSignedNetwork()

        # Act: Run for 2 iterations
        result_df = engine.run(num_iterations=2, network_provider=stub_network)

        # Assert: Verify that .copy() was explicitly called once per iteration
        assert stub_network.copy_count == 2
        assert len(result_df) == 6
        assert list(result_df["iteration"]) == [0, 0, 0, 1, 1, 1]

    def test_run_raises_attribute_error_when_copy_missing(self, mock_analysis_pipeline):
        # Arrange
        engine = SimulationEngine(analysis_pipeline=mock_analysis_pipeline)
        
        # Pass an object that does not implement a .copy() method
        invalid_network_object = object()

        # Act & Assert: Running this must raise an AttributeError during normalization
        with pytest.raises(AttributeError):
            engine.run(num_iterations=1, network_provider=invalid_network_object)

    def test_fallback_index_label_when_index_name_is_none(self):
        # Arrange
        # Create a pipeline that yields a DataFrame with an anonymous index (None)
        def pipeline_with_unnamed_index(network):
            df = pd.DataFrame({"score": [1.0]})
            df.index.name = None
            return df

        engine = SimulationEngine(analysis_pipeline=pipeline_with_unnamed_index)
        mock_network_generator = MagicMock(return_value=MagicMock(spec=SignedNetwork))

        # Act
        result_df = engine.run(num_iterations=1, network_provider=mock_network_generator)

        # Assert: Ensure it falls back to naming the index column "node"
        assert "node" in result_df.columns
        assert list(result_df.columns) == ["iteration", "node", "score"]
