# test_StateKeyGenerator
import pytest
from unittest.mock import MagicMock

from signnet.utils.StateKeyGenerator import StateKeyGenerator
from signnet.models.SignedNetwork import SignedNetwork


class TestStateKeyGenerator:
    """Tests covering the deterministic key generation and builder pattern of StateKeyGenerator."""

    def test_default_prefix_and_empty_generation(self):
        # Arrange
        generator = StateKeyGenerator()
        
        # Act
        key = generator.generate()
        
        # Assert: Default prefix should be 'params' with no extra components
        assert key == "params_"

    def test_custom_prefix(self):
        # Arrange
        generator = StateKeyGenerator(prefix="custom")
        
        # Act
        key = generator.generate()
        
        # Assert: Verify that the custom prefix is correctly applied
        assert key == "custom_"

    def test_add_network(self):
        # Arrange
        generator = StateKeyGenerator(prefix="test")
        
        # Create a mock for SignedNetwork to control node and edge lengths
        mock_network = MagicMock(spec=SignedNetwork)
        mock_network.nodes = [0, 1, 2]       # Length of 3
        mock_network.edges = [(0, 1), (1, 2)] # Length of 2

        # Act
        result = generator.add_network(mock_network)
        key = result.generate()

        # Assert: Method chaining works and string contains lengths
        assert result is generator
        assert key == "test_net_nodes_3_edges_2"

    def test_add_flat_param(self):
        # Arrange
        generator = StateKeyGenerator(prefix="test")

        # Act
        result = generator.add_flat_param(key="max_value", value=100)
        key = result.generate()

        # Assert: Verify flat parameter format and chaining
        assert result is generator
        assert key == "test_max_value_100"

    def test_add_dict_sorting_and_prefix(self):
        # Arrange
        generator = StateKeyGenerator(prefix="test")
        # Unsorted dictionary input
        unordered_params = {"z_param": "last", "a_param": "first", "m_param": "middle"}

        # Act
        # Testing with a custom prefix for the dictionary components
        result = generator.add_dict(parameters=unordered_params, prefix="topo")
        key = result.generate()

        # Assert: Elements must be sorted alphabetically and separated by colons
        assert result is generator
        expected_key = "test_topo_a_param:first_topo_m_param:middle_topo_z_param:last"
        assert key == expected_key

    def test_add_dict_empty(self):
        # Arrange
        generator = StateKeyGenerator(prefix="test")

        # Act
        result = generator.add_dict(parameters={})
        key = result.generate()

        # Assert: An empty dictionary must gracefully return self without modifying components
        assert result is generator
        assert key == "test_"

    def test_add_measures_with_parameters_sorting(self):
        # Arrange
        generator = StateKeyGenerator(prefix="test")
        
        # Unordered selected names
        selected_names = ["Degree", "Betweenness"]
        
        # Runtime parameters containing internal unordered sub-parameters
        runtime_parameters = {
            "Degree": {"k": 4, "p": 0.05},
            "Betweenness": {"normalized": True}
        }

        # Act
        result = generator.add_measures_with_parameters(
            selected_names=selected_names, 
            runtime_parameters=runtime_parameters
        )
        key = result.generate()

        # Assert: Measures and sub-parameters must be resolved alphabetically
        assert result is generator
        # Order details: Betweenness comes before Degree. 'k' comes before 'p'.
        expected_key = "test_Betweenness_normalized:True_Degree_k:4_p:0.05"
        assert key == expected_key

    def test_full_builder_chaining_integration(self):
        # Arrange: Setup a complex scenario mixing multiple components
        generator = StateKeyGenerator(prefix="app")
        
        mock_network = MagicMock(spec=SignedNetwork)
        mock_network.nodes = [1, 2, 3, 4]
        mock_network.edges = [(1, 2)]
        
        dict_params = {"beta": 0.5, "alpha": 1}

        # Act: Execute sequential method chaining in a single statement
        key = (generator
               .add_network(mock_network)
               .add_flat_param("mode", "strict")
               .add_dict(dict_params, prefix="config")
               .generate())

        # Assert: Verify that components assemble seamlessly in execution order
        expected_key = "app_net_nodes_4_edges_1_mode_strict_config_alpha:1_config_beta:0.5"
        assert key == expected_key
