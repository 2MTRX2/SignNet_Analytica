# test_LoadingRegistry.py
import pytest

from signnet.io.LoadingRegistry import (
    REPRESENTATION_REGISTRY,
    STRATEGY_REGISTRY,
    EXTENSION_TO_FORMAT,
    get_available_representations,
    get_available_file_types
)
from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser
from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_loading.ExcelStrategy import ExcelStrategy
from signnet.io.data_loading.JsonStrategy import JsonStrategy

# =====================================================================
# LOADING REGISTRY TESTS
# =====================================================================

def test_registries_contain_correct_mappings():
    assert REPRESENTATION_REGISTRY["Edge List"] is EdgeListNormaliser
    assert REPRESENTATION_REGISTRY["Adjacency Matrix"] is AdjacencyMatrixNormaliser
    assert len(REPRESENTATION_REGISTRY) == 2

    assert STRATEGY_REGISTRY["csv"] is CsvStrategy
    assert STRATEGY_REGISTRY["excel"] is ExcelStrategy
    assert STRATEGY_REGISTRY["json"] is JsonStrategy
    assert len(STRATEGY_REGISTRY) == 3


def test_extension_to_format_mappings():
    assert EXTENSION_TO_FORMAT["csv"] == "CSV"
    assert EXTENSION_TO_FORMAT["xlsx"] == "EXCEL"
    assert EXTENSION_TO_FORMAT["xls"] == "EXCEL"
    assert EXTENSION_TO_FORMAT["json"] == "JSON"
    assert len(EXTENSION_TO_FORMAT) == 4


def test_get_available_representations():
    # ACT
    representations = get_available_representations()

    # ASSERT
    expected = ["Edge List", "Adjacency Matrix"]
    assert representations == expected


def test_get_available_file_types():
    # ACT
    file_types = get_available_file_types()

    # ASSERT
    expected = ["CSV", "EXCEL", "JSON"]
    assert file_types == expected

    for fmt in file_types:
        assert fmt.isupper()
