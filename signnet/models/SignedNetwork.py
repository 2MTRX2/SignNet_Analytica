# StaticSignedNetwork.py
import pandas as pd
from typing import Set, List
from typing import Optional, Iterable

class SignedNetwork:
    """Represents the canonical in-memory representation of a signed network with an edge list.

    The class encapsulates the network topology as a standardized edge list
    (source, target, sign) and provides read-only access to its structural
    properties. It serves as the central domain object for all subsequent
    analysis components.
    """

    def __init__(self, edges: pd.DataFrame, nodes: Optional[Iterable]=None, directed: bool = False):

        self._directed = directed
        
        # Make a copy of the dataframe edgelist and save only the relevant columns (pandas dataframe)
        if edges.empty:
            self._edges = pd.DataFrame(columns=['source', 'target', 'sign'])
        else: 
            self._edges = edges[['source', 'target', 'sign']].copy().reset_index(drop=True)
        
        # One-time calculation of the existing nodes saved in a set and a list for quick search 
        if nodes is None:
            nodes = (set(edges["source"]) | set(edges["target"]))

        self._validate(edges, nodes)

        self._nodes_set: Set = set(nodes)
        self._nodes_list: List = sorted(list(self._nodes_set))

    @staticmethod
    def _validate(edges: pd.DataFrame, nodes: Optional[Iterable]):
        required = {"source", "target", "sign"}
        missing = required - set(edges.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        if edges.empty and (nodes is None or len(list(nodes)) == 0):
            raise ValueError("Network contains no edges and no nodes.")
        
        if edges.empty:
            raise ValueError("Network contains no edges.")
        if edges[["source", "target"]].isnull().any().any():
            raise ValueError("Source and target nodes must not be null.")
        if edges["sign"].isnull().any():
            raise ValueError("Edge signs must not be null.")

        
    def __repr__(self):

        return (
            f"SignedNetwork("
            f"directed={self.directed}, "
            f"nodes={self.number_of_nodes}, "
            f"edges={self.number_of_edges})"
        )
        
    @property
    def directed(self):
        return self._directed

    @property
    def edges(self) -> pd.DataFrame:
        """Returns the structural edge list."""
        return self._edges.copy()  # makes a copy of the edge list so that unwanted manipulation does not happen (if the application is too slow, this needs to be changed)
    
    @property
    def nodes(self) -> tuple:
        """Returns an unchangeable (immutable) tuple of all unique nodes."""
        return tuple(self._nodes_list)

    @property
    def number_of_nodes(self) -> int:
        """Returns the total number of unique nodes."""
        return len(self._nodes_set)

    @property
    def number_of_edges(self) -> int:
        """Returns the total number of signed edges."""
        return len(self._edges)
    
    def has_node(self, node) -> bool:
        return node in self._nodes_set
    
    def copy(self):
        return SignedNetwork(
            self._edges.copy(),
            directed=self._directed
        )
