# test_NetworkGenerator.py
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
import networkx as nx

from signnet.models.NetworkGenerator import NetworkGenerator
from signnet.models.SignedNetwork import SignedNetwork


@pytest.fixture
def mock_topology_registry():
    """Mocking Topology Registry"""
    with patch("signnet.models.NetworkGenerator.TopologyRegistry") as mock_registry:
        # Simulating Topologies
        mock_registry.get_available_topologies.return_value = {"Test-Topology", "Small-World"}
        
        # Simulating NetworkX graph builder
        def dummy_generator(n, **kwargs):
            G = nx.Graph()
            G.add_edges_from([(0, 1), (1, 2)])
            return G
            
        mock_registry.get_topology_data.return_value = {"func": dummy_generator}
        yield mock_registry


class TestNetworkGeneratorInitialization:
    """Tests the validations at the class initialisation"""

    def test_init_success(self, mock_topology_registry):
        # Arrange & Act
        generator = NetworkGenerator(topology_name="Test-Topology", n=10, neg_ratio=0.3, custom_param="value")
        
        # Assert
        assert generator.topology_name == "Test-Topology"
        assert generator.n == 10
        assert generator.neg_ratio == 0.3
        assert generator.kwargs == {"custom_param": "value"}

    def test_init_raises_value_error_for_invalid_topology(self, mock_topology_registry):
        # Act & Assert
        with pytest.raises(ValueError, match="Topology 'Unknown' is not available"):
            NetworkGenerator(topology_name="Unknown", n=10, neg_ratio=0.5)

    @pytest.mark.parametrize("invalid_n", [2, 1, 0, -5])
    def test_init_raises_value_error_for_low_node_count(self, mock_topology_registry, invalid_n):
        # Act & Assert
        with pytest.raises(ValueError, match="The number of nodes n must be at least 3"):
            NetworkGenerator(topology_name="Test-Topology", n=invalid_n, neg_ratio=0.5)

    @pytest.mark.parametrize("invalid_ratio", [-0.1, 1.1, 2.0])
    def test_init_raises_value_error_for_out_of_bounds_neg_ratio(self, mock_topology_registry, invalid_ratio):
        # Act & Assert
        with pytest.raises(ValueError, match="The conflict rate .* must be inside"):
            NetworkGenerator(topology_name="Test-Topology", n=10, neg_ratio=invalid_ratio)


class TestNetworkGeneratorNetworkCreation:
    """Tests the generation of networks of the method `create_random_signed_network`."""

    def test_create_random_signed_network_structure(self, mock_topology_registry):
        # Arrange
        n = 3
        generator = NetworkGenerator(topology_name="Test-Topology", n=n, neg_ratio=0.5)
        
        # Act
        result = generator.create_random_signed_network()
        
        # Assert
        assert isinstance(result, SignedNetwork)
        assert result.nodes == (0, 1, 2)
        assert result.directed is False
        
        assert isinstance(result.edges, pd.DataFrame)
        assert len(result.edges) == 2  
        assert list(result.edges.columns) == ["source", "target", "sign"]

    def test_create_random_signed_network_all_positive(self, mock_topology_registry):
        # Arrange
        generator = NetworkGenerator(topology_name="Test-Topology", n=3, neg_ratio=0.0)
        
        # Act
        result = generator.create_random_signed_network()
        
        # Assert
        assert (result.edges["sign"] == 1.0).all()

    def test_create_random_signed_network_all_negative(self, mock_topology_registry):
        # Arrange
        generator = NetworkGenerator(topology_name="Test-Topology", n=3, neg_ratio=1.0)
        
        # Act
        result = generator.create_random_signed_network()
        
        # Assert
        assert (result.edges["sign"] == -1.0).all()
