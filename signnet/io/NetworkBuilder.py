# NetworkBuilder.py
import streamlit as st

from signnet.models.SignedNetwork import SignedNetwork
from signnet.io.LoadingRegistry import REPRESENTATION_REGISTRY
from signnet.io.LoadingRegistry  import STRATEGY_REGISTRY

# Caching of the parameters of the function and the returned object
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
    Dynamically loads raw network data and builds a structured SignedNetwork object.

    Uses a factory/registry pattern to resolve the appropriate file parser and 
    structural representation format at runtime. The output is cached via Streamlit 
    to optimize performance during application re-runs.

    Args:
        file_buffer (BytesIO | StringIO): Raw file stream from upload or registry.
        file_type (str): Format extension (e.g., 'csv', 'excel', 'json').
        representation_type (str): Input structure ('Edge List' or 'Adjacency Matrix').
        is_directed (bool): True for directed edges, False for undirected.
        source_col (str, optional): Source node column name. Defaults to 'source'.
        target_col (str, optional): Target node column name. Defaults to 'target'.
        sign_col (str, optional): Edge sign column name. Defaults to 'sign'.

    Returns:
        SignedNetwork: Fully initialized signed network containing nodes and edges.

    Raises:
        ValueError: If the `representation_type` is not found in REPRESENTATION_REGISTRY.
        ValueError: If the `file_type` is not found in STRATEGY_REGISTRY.
    """
    if representation_type not in REPRESENTATION_REGISTRY:
        raise ValueError(f"Unsupported network representation: {representation_type}")

    reprsentation_class = REPRESENTATION_REGISTRY[representation_type]

    if representation_type == "Edge List":
        representation = reprsentation_class(source_col=source_col, target_col=target_col, sign_col=sign_col)
    else:
        representation = reprsentation_class(directed=is_directed)

    fmt = file_type.lower()

    if fmt not in STRATEGY_REGISTRY:
        raise ValueError(f"Unsupported file format configuration: {file_type}")

    loader_class = STRATEGY_REGISTRY[fmt]
    loader = loader_class(representation)

    network_data = loader.load(file_buffer)
    return SignedNetwork(edges=network_data.edges, nodes=network_data.nodes, directed=is_directed)
