# LoadingRegistry.py
from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser
from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_loading.ExcelStrategy import ExcelStrategy
from signnet.io.data_loading.JsonStrategy import JsonStrategy

"""Central structural configuration registers for handling framework I/O operations.

Consolidates the available structural representation mappings and file-loading strategies 
to achieve a format-agnostic network ingestion pipeline. This registry acts as the 
decoupled binding layer between raw file system formats and internal data normalization engines.
"""

# Central definition of representations
REPRESENTATION_REGISTRY = {
    "Edge List": EdgeListNormaliser,
    "Adjacency Matrix": AdjacencyMatrixNormaliser
}

# Central definition of loading strategies
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