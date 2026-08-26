# test_NetworkBuilder.py
import pytest
from unittest.mock import MagicMock, patch

from signnet.models.SignedNetwork import SignedNetwork
from signnet.io.data_representation.NetworkData import NetworkData
from signnet.io.NetworkBuilder import load_and_build_network

# =====================================================================
# NETWORK BUILDER TESTS
# =====================================================================

@pytest.fixture
def mock_registries():
    # needed to check representation type if-else structure
    mock_edge_list_cls = MagicMock()
    mock_matrix_cls = MagicMock()
    # returns the instance of this class and is instantiated with the mocks above
    mock_loader_cls = MagicMock()

    # return of the instance of the class itself
    mock_loader_instance = MagicMock()
    mock_loader_cls.return_value = mock_loader_instance

    # return of the network object on instance level
    fake_network_data = NetworkData(edges="fake_edges", nodes="fake_nodes")
    mock_loader_instance.load.return_value = fake_network_data

    # mock of the signed network class
    mock_signed_network_cls = MagicMock()
    mock_network_instance = MagicMock()
    mock_signed_network_cls.return_value = mock_network_instance

    with patch("signnet.io.NetworkBuilder.REPRESENTATION_REGISTRY", {
        "Edge List": mock_edge_list_cls,
        "Adjacency Matrix": mock_matrix_cls
    }), patch("signnet.io.NetworkBuilder.STRATEGY_REGISTRY", {
        "csv": mock_loader_cls,
        "CSV": mock_loader_cls
    }), patch("signnet.io.NetworkBuilder.SignedNetwork", mock_signed_network_cls):
        
        yield {
            "edge_list_cls": mock_edge_list_cls,
            "matrix_cls": mock_matrix_cls,
            "loader_cls": mock_loader_cls,
            "loader_instance": mock_loader_instance,
            "signed_network_cls": mock_signed_network_cls,
            "network_instance": mock_network_instance
        }


def test_load_and_build_network_edge_list_flow(mock_registries):
    # ARRANGE
    file_buffer = "dummy_buffer"
    
    # ACT
    result = load_and_build_network(
        file_buffer=file_buffer,
        file_type="csv",
        representation_type="Edge List",
        is_directed=True,
        source_col="src",
        target_col="dst",
        sign_col="weight"
    )

    # ASSERT
    # 1. right column mapping instantiation and check if the representation handler was only ivoked once
    mock_registries["edge_list_cls"].assert_called_once_with(
        source_col="src", target_col="dst", sign_col="weight"
    )
    
    # 2. initialisation of representation handler and check if the loader was only invoked once
    mock_repr_instance = mock_registries["edge_list_cls"].return_value
    mock_registries["loader_cls"].assert_called_once_with(mock_repr_instance)
    
    # 3. check if load method invoked only once
    mock_registries["loader_instance"].load.assert_called_once_with(file_buffer)

    mock_registries["signed_network_cls"].assert_called_once_with(
        edges="fake_edges",
        nodes="fake_nodes",
        directed=True
    )

    assert result == mock_registries["network_instance"]


def test_load_and_build_network_matrix_flow(mock_registries):
    # ARRANGE
    file_buffer = "dummy_buffer"

    # ACT
    result = load_and_build_network(
        file_buffer=file_buffer,
        file_type="CSV", 
        representation_type="Adjacency Matrix",
        is_directed=False
    )

    # ASSERT
    mock_registries["matrix_cls"].assert_called_once_with(directed=False)

    mock_registries["signed_network_cls"].assert_called_once_with(
        edges="fake_edges",
        nodes="fake_nodes",
        directed=False
    )

    assert result == mock_registries["network_instance"]


def test_load_and_build_network_unsupported_representation(mock_registries):
    with pytest.raises(ValueError, match="Unsupported network representation"):
        load_and_build_network(
            file_buffer="buf",
            file_type="csv",
            representation_type="Invalid Type",
            is_directed=True
        )
    mock_registries["loader_instance"].load.assert_not_called()
    mock_registries["signed_network_cls"].assert_not_called()


def test_load_and_build_network_unsupported_file_type(mock_registries):
    with pytest.raises(ValueError, match="Unsupported file format configuration"):
        load_and_build_network(
            file_buffer="buf",
            file_type="xml", 
            representation_type="Edge List",
            is_directed=True
        )
    mock_registries["loader_instance"].load.assert_not_called()
    mock_registries["signed_network_cls"].assert_not_called()
