# LoadingRegistry.py

from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser
from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_loading.ExcelStrategy import ExcelStrategy
from signnet.io.data_loading.JsonStrategy import JsonStrategy

# 1. Central definition of representations
REPRESENTATION_REGISTRY = {
    "Edge List": EdgeListNormaliser,
    "Adjacency Matrix": AdjacencyMatrixNormaliser
}

# 2. Central definition of loading strategies
STRATEGY_REGISTRY = {
    "csv": CsvStrategy,
    "excel": ExcelStrategy,
    "json": JsonStrategy
}

EXTENSION_TO_FORMAT = {
    "csv": "CSV",
    "xlsx": "EXCEL",
    "xls": "EXCEL",
    "json": "JSON"
}


def get_available_representations() -> list[str]:
    """Returns all valid representaion types."""
    return list(REPRESENTATION_REGISTRY.keys())

def get_available_file_types() -> list[str]:
    """Returns all format loading strategies in capital letters"""
    return [fmt.upper() for fmt in STRATEGY_REGISTRY.keys()]