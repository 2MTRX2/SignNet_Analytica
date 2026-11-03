# LoadingService.py
from typing import Union
from io import BytesIO, StringIO

from signnet.models.SignedNetwork import SignedNetwork
from signnet.io.LoadingRegistry import REPRESENTATION_REGISTRY, STRATEGY_REGISTRY

class NetworkService: 
    """
    Executes raw file parsing pipelines and handles structural domain-network construction.
    """
    def __init__(self):
        pass

    def load_and_build_network(
        self,
        file_buffer: Union[BytesIO, StringIO],
        file_type: str,
        representation_type: str,
        is_directed: bool,
        source_col: str = 'source',
        target_col: str = 'target',
        sign_col: str = 'sign'
    ) -> SignedNetwork:
        """Dynamically loads raw network data and builds a structured SignedNetwork object.

        Args:
            file_buffer (BytesIO | StringIO): Raw file stream or IO buffer from the user upload component.
            file_type (str): Format extension mapping to registry strategies (e.g., 'csv', 'excel', 'json').
            representation_type (str): Input graph layout mapping to structural types ('Edge List' or 'Adjacency Matrix').
            is_directed (bool): True if the network edges should be processed as directed, False for undirected.
            source_col (str, optional): Source node column name for Edge List mapping. Defaults to 'source'.
            target_col (str, optional): Target node column name for Edge List mapping. Defaults to 'target'.
            sign_col (str, optional): Edge valence/sign column name for Edge List mapping. Defaults to 'sign'.

        Returns:
            SignedNetwork: Fully initialized canonical signed network containing aligned nodes and edges.

        Raises:
            ValueError: If the requested `representation_type` is not supported by REPRESENTATION_REGISTRY.
            ValueError: If the requested `file_type` parser configuration is not supported by STRATEGY_REGISTRY.
        """
        # Validation
        if representation_type not in REPRESENTATION_REGISTRY:
            raise ValueError(f"Unsupported network representation: {representation_type}")

        representation_class = REPRESENTATION_REGISTRY[representation_type]

        # Instantiation
        if representation_type == "Edge List":
            representation = representation_class(
                source_col=source_col, 
                target_col=target_col, 
                sign_col=sign_col
            )
        else:
            representation = representation_class(directed=is_directed)

        # Validation
        fmt = file_type.lower()
        if fmt not in STRATEGY_REGISTRY:
            raise ValueError(f"Unsupported file format configuration: {file_type}")

        # Loading
        loader_class = STRATEGY_REGISTRY[fmt]
        loader = loader_class(representation)
        network_data = loader.load(file_buffer)

        # Return of the SignedNetwork
        return SignedNetwork(
            edges=network_data.edges, 
            nodes=network_data.nodes, 
            directed=is_directed
        )
