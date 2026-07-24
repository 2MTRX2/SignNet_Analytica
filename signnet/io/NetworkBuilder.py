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
    """Dynamically loads raw network data and builds a structured SignedNetwork object.

    This function automatically selects the appropriate file parsing strategy and 
    structural normaliser based on the provided configuration. The execution is 
    cached via Streamlit to ensure fast script re-runs when parameters remain unchanged.

    Args:
        file_buffer (BytesIO / StringIO): The raw file stream uploaded by the user or from the data registry.
        file_type (str): The file extension format (e.g., 'csv', 'excel', 'json').
        representation_type (str): Structural input format, either 'Edge List' 
            or 'Adjacency Matrix'.
        is_directed (bool): True if the network edges have a specific direction, 
            False otherwise.
        source_col (str, optional): Name of the column representing the source nodes. 
            Defaults to 'source'. Only used for 'Edge List'.
        target_col (str, optional): Name of the column representing the target nodes. 
            Defaults to 'target'. Only used for 'Edge List'.
        sign_col (str, optional): Name of the column representing the edge signs 
            (positive/negative). Defaults to 'sign'. Only used for 'Edge List'.

    Raises:
        ValueError: If `representation_type` is not 'Edge List' or 'Adjacency Matrix'.
        ValueError: If `file_type` is not supported (not 'csv', 'excel', or 'json').

    Returns:
        SignedNetwork: An immutable, fully built and structured signed network 
            instance containing nodes and edges.
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
