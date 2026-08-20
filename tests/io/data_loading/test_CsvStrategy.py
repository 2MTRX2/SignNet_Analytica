# test_CsvStrategy.py
import io as io_module
from unittest.mock import MagicMock
 
import pandas as pd
import pytest

from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_representation.RepresentationNormaliser import RepresentationNormaliser

class TestCsvStrategy:
    """Tests for CsvStrategy.load(). The RepresentationNormaliser-Dependency
    is mocked to test the CsvStrategy isolated."""
 
    @pytest.fixture
    def mock_representation(self):
        mock = MagicMock(spec=RepresentationNormaliser)
        return mock
 
    @pytest.fixture
    def expected_edge_list(self):
        return pd.DataFrame({
            "source": ["A", "B"],
            "target": ["B", "C"],
            "sign": [1, -1],
        })
 
    def test_load_delegates_parsed_dataframe_to_representation(
        self, tmp_path, mock_representation, expected_edge_list
    ):
        """Happy path: Csv gets correctly read and delegates the formatting to the RepresentationNormaliser."""
        csv_file = tmp_path / "network.csv"
        csv_file.write_text("source,target,sign\nA,B,1\nB,C,-1\n")
        mock_representation.to_edge_list.return_value = expected_edge_list
 
        strategy = CsvStrategy(representation=mock_representation)
        result = strategy.load(str(csv_file))
 
        assert mock_representation.to_edge_list.call_count == 1
        called_arg = mock_representation.to_edge_list.call_args[0][0]
        assert isinstance(called_arg, pd.DataFrame)
        assert list(called_arg.columns) == ["source", "target", "sign"]
        assert called_arg.shape == (2, 3)
 
        pd.testing.assert_frame_equal(result, expected_edge_list)
 
    def test_load_returns_exact_object_from_representation(
        self, tmp_path, mock_representation
    ):
        """Returning value: The return value of the RepresentationNormaliser gets returned unchanged."""
        csv_file = tmp_path / "network.csv"
        csv_file.write_text("a,b,c\n1,2,3\n")
        sentinel = pd.DataFrame({"source": [], "target": [], "sign": []})
        mock_representation.to_edge_list.return_value = sentinel
 
        strategy = CsvStrategy(representation=mock_representation)
        result = strategy.load(str(csv_file))
 
        assert result is sentinel
 
    def test_load_with_headers_only_produces_empty_dataframe(
        self, tmp_path, mock_representation
    ):
        """Edge Case: Csv contains only headers, no data."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("source,target,sign\n")
        mock_representation.to_edge_list.return_value = pd.DataFrame(
            columns=["source", "target", "sign"]
        )
 
        strategy = CsvStrategy(representation=mock_representation)
        strategy.load(str(csv_file))
 
        called_arg = mock_representation.to_edge_list.call_args[0][0]
        assert called_arg.empty
        assert list(called_arg.columns) == ["source", "target", "sign"]
 
    def test_load_with_nonexistent_file_raises_and_does_not_call_representation(
        self, tmp_path, mock_representation
    ):
        """Edge case: File does not exist, RepresentationNormaliser does not get called because of error"""
        missing_file = tmp_path / "does_not_exist.csv"
 
        strategy = CsvStrategy(representation=mock_representation)
 
        with pytest.raises(FileNotFoundError):
            strategy.load(str(missing_file))
 
        mock_representation.to_edge_list.assert_not_called()
 
    def test_load_accepts_file_like_object(self, mock_representation, expected_edge_list):
        """Edge case: file_source is a file-like object (e.g. Streamlit Upload)."""
        mock_representation.to_edge_list.return_value = expected_edge_list
        file_like = io_module.StringIO("source,target,sign\nA,B,1\nB,C,-1\n")
 
        strategy = CsvStrategy(representation=mock_representation)
        result = strategy.load(file_like)
 
        called_arg = mock_representation.to_edge_list.call_args[0][0]
        assert called_arg.shape == (2, 3)
        pd.testing.assert_frame_equal(result, expected_edge_list)
 
    def test_load_with_malformed_csv_raises_parser_error(self, tmp_path, mock_representation):
        """Edge case: inconsistent column number -> pandas ParserError."""
        csv_file = tmp_path / "malformed.csv"
        csv_file.write_text("source,target,sign\nA,B,1,extra_value\n")
 
        strategy = CsvStrategy(representation=mock_representation)
 
        with pytest.raises(pd.errors.ParserError):
            strategy.load(str(csv_file))
 
        mock_representation.to_edge_list.assert_not_called()