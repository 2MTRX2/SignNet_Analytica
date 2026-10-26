# test_TopologyRegistry.py
import pytest
import networkx as nx
from typing import Callable

from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry


class TestTopologyRegistryMethods:
    """Tests for the primary class methods of TopologyRegistry."""

    def test_get_available_topologies(self):
        # Act
        topologies = TopologyRegistry.get_available_topologies()

        # Assert: Verify it returns a list containing all the expected 4 hardcoded topologies
        assert isinstance(topologies, list)
        assert len(topologies) == 4
        assert "Random network G(N, M) (Erdős-Rényi)" in topologies
        assert "Random network G(N, p) (Erdős-Rényi)" in topologies
        assert "Scale-Free (Barabási-Albert)" in topologies
        assert "Small-World (Watts-Strogatz)" in topologies

    def test_get_topology_data_success(self):
        # Arrange
        topology_name = "Random network G(N, p) (Erdős-Rényi)"

        # Act
        data = TopologyRegistry.get_topology_data(topology_name)

        # Assert: Ensure metadata structure is correct and maps to the right NetworkX function
        assert isinstance(data, dict)
        assert "func" in data
        assert "params" in data
        assert data["func"] == nx.erdos_renyi_graph
        assert "p" in data["params"]

    def test_get_topology_data_raises_value_error(self):
        # Act & Assert: Verify it rejects unregistered names with a proper ValueError
        with pytest.raises(ValueError, match="Topology name 'NonExistent' is not registered"):
            TopologyRegistry.get_topology_data("NonExistent")


class TestTopologyRegistryLambdas:
    """Tests to evaluate the dynamic lambda logic for max and value boundaries across different sizes of N."""

    def test_erdos_renyi_m_lambdas(self):
        # Arrange
        data = TopologyRegistry.get_topology_data("Random network G(N, M) (Erdős-Rényi)")
        m_spec = data["params"]["m"]
        max_lambda: Callable = m_spec["max"]
        value_lambda: Callable = m_spec["value"]

        # Assert dynamic maximum: for N=4, max edges = (4 * 3) / 2 = 6
        assert max_lambda(n=4) == 6
        assert max_lambda(n=1) == 1

        # Assert dynamic fallback values
        assert value_lambda(n=4, orig_m=3) == 3  # Should preserve original M if provided
        assert value_lambda(n=100, orig_m=None) == 10  # Cap at default 10 for big networks
        assert value_lambda(n=3, orig_m=None) == 3  # Cap at max possible edges (3*2/2 = 3) for small N

    def test_barabasi_albert_lambdas(self):
        # Arrange
        data = TopologyRegistry.get_topology_data("Scale-Free (Barabási-Albert)")
        m_spec = data["params"]["m"]
        max_lambda: Callable = m_spec["max"]
        value_lambda: Callable = m_spec["value"]

        # Assert boundaries: Barabási-Albert requires attachment edges m <= N - 1
        assert max_lambda(n=10) == 9
        assert value_lambda(n=5, orig_m=None) == 2  # Default should be 2 if N is large enough
        assert value_lambda(n=2, orig_m=None) == 1  # Degrade gracefully to 1 edge if N=2

    def test_watts_strogatz_lambdas(self):
        # Arrange
        data = TopologyRegistry.get_topology_data("Small-World (Watts-Strogatz)")
        k_spec = data["params"]["k"]
        max_lambda: Callable = k_spec["max"]
        value_lambda: Callable = k_spec["value"]

        # Assert boundaries: Watts-Strogatz ring topology constraints based on N parity
        assert max_lambda(n=6) == 4  # Even N: N - 2
        assert max_lambda(n=5) == 4  # Odd N: N - 1

        # Assert dynamic value logic
        assert value_lambda(n=10, orig_m=None) == 4  # Ideal default target is 4
        assert value_lambda(n=3, orig_m=None) == 2  # Scale down to 2 if N is too small
