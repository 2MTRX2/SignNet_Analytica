# NetworkBuilder.py

import streamlit as st
from signnet.models.SignedNetwork import SignedNetwork
from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser
from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_loading.ExcelStrategy import ExcelStrategy
from signnet.io.data_loading.JsonStrategy import JsonStrategy

@st.cache_data(show_spinner="Processing and building signed network...")
def load_and_build_network(
    file_buffer, 
    file_type: str, 
    representation_type: str, 
    is_directed: bool, 
    source_col: str = 'source',  
    target_col: str = 'target',
    sign_col: str = 'sign'
) -> SignedNetwork:
    """
    Selects the appropriate file strategy and normaliser dynamically.
    Caches the resulting SignedNetwork to ensure high performance.
    """
    if representation_type == "Edge List":
        representation = EdgeListNormaliser(source_col=source_col, target_col=target_col, sign_col=sign_col)
    elif representation_type == "Adjacency Matrix":
        representation = AdjacencyMatrixNormaliser(directed=is_directed)
    else:
        raise ValueError(f"Unsupported network representation: {representation_type}")

    fmt = file_type.lower()
    if fmt == "csv":
        loader = CsvStrategy(representation)
    elif fmt == "excel":
        loader = ExcelStrategy(representation)
    elif fmt == "json":
        loader = JsonStrategy(representation)
    else:
        raise ValueError(f"Unsupported file format configuration: {file_type}")

    network_data = loader.load(file_buffer)
    return SignedNetwork(edges=network_data.edges, nodes=network_data.nodes, directed=is_directed)
