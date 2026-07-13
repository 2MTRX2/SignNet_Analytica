# test_AdjacencyMatrixNormaliser.py
import io as io_module
from unittest.mock import MagicMock
 
import pandas as pd
import pytest

from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser

class TestAdjacencyMatrixNormaliser:
    """Tests for the AdjacencyMatrixNormaliser.to_edge_list(). The function
    transform_matrix_to_edgelist from utils.matrix_helpers is mocked, because she is outside
    of the responsibility of that class."""
 
    @pytest.fixture
    def patched_transform(self, monkeypatch):
        """Patching of the function transform_matrix_to_edgelist inside the namespace of this module
        in which the funciton was imported."""
        mock_fn = MagicMock()
        monkeypatch.setattr(
            AdjacencyMatrixNormaliser, "transform_matrix_to_edgelist", mock_fn
        )
        return mock_fn
 
    def test_to_edge_list_sets_first_column_as_index_and_delegates(
        self, patched_transform
    ):
        """Happy path: first column as an index, the rest delegated to transform_matrix_to_edgelist."""
        raw_df = pd.DataFrame({
            "node": ["A", "B", "C"],
            "A": [0, 1, -1],
            "B": [1, 0, 1],
            "C": [-1, 1, 0],
        })
        expected_result = pd.DataFrame({
            "source": ["A", "B"], "target": ["B", "C"], "sign": [1, 1]
        })
        patched_transform.return_value = expected_result
 
        normaliser = AdjacencyMatrixNormaliser()
        result = normaliser.to_edge_list(raw_df)
 
        assert patched_transform.call_count == 1

        # taking the entry matrice and check if structure is correct
        matrix_arg = patched_transform.call_args[0][0]
        assert list(matrix_arg.index) == ["A", "B", "C"]
        assert list(matrix_arg.columns) == ["A", "B", "C"]
        assert matrix_arg.loc["A", "B"] == 1
        assert matrix_arg.loc["A", "C"] == -1
 
        # check if the matrix gets properly returned
        pd.testing.assert_frame_equal(result, expected_result)
 
    def test_to_edge_list_with_single_node_matrix(self, patched_transform):
        """Grenzfall: Matrix mit nur einem Knoten (1x1)."""
        raw_df = pd.DataFrame({"node": ["A"], "A": [0]})
        patched_transform.return_value = pd.DataFrame(
            columns=["source", "target", "sign"]
        )
 
        normaliser = AdjacencyMatrixNormaliser()
        normaliser.to_edge_list(raw_df)
 
        matrix_arg = patched_transform.call_args[0][0]
        assert matrix_arg.shape == (1, 1)
        assert list(matrix_arg.index) == ["A"]
 
    def test_to_edge_list_with_matrix_containing_only_zero_entries(
        self, patched_transform
    ):
        """Grenzfall: alle Werte 0 -> keine Kanten. transform_matrix_to_edgelist
        ist dafür zuständig, das zu filtern; hier prüfen wir nur die korrekte
        Weitergabe der vollständigen (noch ungefilterten) Matrix."""
        raw_df = pd.DataFrame({
            "node": ["A", "B"],
            "A": [0, 0],
            "B": [0, 0],
        })
        patched_transform.return_value = pd.DataFrame(
            columns=["source", "target", "sign"]
        )
 
        normaliser = AdjacencyMatrixNormaliser()
        result = normaliser.to_edge_list(raw_df)
 
        matrix_arg = patched_transform.call_args[0][0]
        assert (matrix_arg.values == 0).all()
        assert result.empty
 
    def test_to_edge_list_with_no_data_columns_raises_or_delegates_empty(
        self, patched_transform
    ):
        """Grenzfall: DataFrame besitzt nur die Label-Spalte, keine weiteren
        Spalten (leere Matrix ohne Kanteninformation)."""
        raw_df = pd.DataFrame({"node": ["A", "B"]})
        patched_transform.return_value = pd.DataFrame(
            columns=["source", "target", "sign"]
        )
 
        normaliser = AdjacencyMatrixNormaliser()
        normaliser.to_edge_list(raw_df)
 
        matrix_arg = patched_transform.call_args[0][0]
        assert matrix_arg.shape[1] == 0
        assert list(matrix_arg.index) == ["A", "B"]
 
    def test_to_edge_list_returns_exact_object_from_transform_function(
        self, patched_transform
    ):
        """Der Rückgabewert von transform_matrix_to_edgelist wird unverändert
        durchgereicht."""
        raw_df = pd.DataFrame({"node": ["A", "B"], "A": [0, 1], "B": [1, 0]})
        sentinel = pd.DataFrame({"source": ["A"], "target": ["B"], "sign": [1]})
        patched_transform.return_value = sentinel
 
        normaliser = AdjacencyMatrixNormaliser()
        result = normaliser.to_edge_list(raw_df)
 
        assert result is sentinel
 
    @pytest.mark.parametrize("n_nodes", [2, 3, 5])
    def test_to_edge_list_preserves_square_matrix_shape_for_various_sizes(
        self, patched_transform, n_nodes
    ):
        """Grenzfall/Parametrisiert: unterschiedliche Netzwerkgrößen führen zu
        korrekt geformten quadratischen Matrizen."""
        labels = [f"N{i}" for i in range(n_nodes)]
        data = {"node": labels}
        for label in labels:
            data[label] = [0] * n_nodes
        raw_df = pd.DataFrame(data)
        patched_transform.return_value = pd.DataFrame(
            columns=["source", "target", "sign"]
        )
 
        normaliser = AdjacencyMatrixNormaliser()
        normaliser.to_edge_list(raw_df)
 
        matrix_arg = patched_transform.call_args[0][0]
        assert matrix_arg.shape == (n_nodes, n_nodes)
        assert list(matrix_arg.index) == labels
        assert list(matrix_arg.columns) == labels