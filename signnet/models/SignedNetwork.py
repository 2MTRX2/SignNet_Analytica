# StaticSignedNetwork.py
import pandas as pd
from typing import Set, List
from typing import Optional, Iterable, Any

class SignedNetwork:
    """
    Represents the canonical domain model of a signed network utilizing a flat edge list structure.

    This class encapsulates the network topology within an optimized pandas DataFrame and 
    provides read-only access to its mathematical and structural properties. It acts as the 
    central, immutable data gateway for all downstream analytics, centrality measures, and 
    matrix factories within the framework.
    """
    def __init__(self, edges: pd.DataFrame, nodes: Optional[Iterable]=None, directed: bool = False):
        self._directed = directed

        self._validate(edges, nodes)
        
        # Make a copy of the dataframe edgelist and save only the relevant columns (pandas dataframe)
        if edges.empty:
            self._edges = pd.DataFrame(columns=['source', 'target', 'sign'])
        else: 
            self._edges = edges[['source', 'target', 'sign']].copy().reset_index(drop=True)
        
        # One-time calculation of the existing nodes saved in a set and a list for quick search 
        if nodes is None:
            nodes = (set(edges["source"]) | set(edges["target"]))

        self._nodes_set: Set = set(nodes)
        self._nodes_list: List = sorted(list(self._nodes_set))

    @staticmethod
    def _validate(edges: pd.DataFrame, nodes: Optional[Iterable]):
        """
        Internal static validator that enforces strict integrity rules over the structural inputs.

        Checks for the presence of mandatory schema columns, verifies that the network contains 
        active structural elements, and asserts that neither topology coordinates nor edge 
        signs contain invalid null definitions.

        Args:
            edges (pd.DataFrame): The raw edge list DataFrame undergoing structural validation.
            nodes (Optional[Iterable]): The sequence of node identifiers undergoing validation.

        Raises:
            ValueError: If mandatory columns are missing, data structures are empty, or 
                critical fields contain null elements.
        """
        required = {"source", "target", "sign"}
        missing = required - set(edges.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        if edges.empty and (nodes is None or len(list(nodes)) == 0):
            raise ValueError("Network contains no edges and no nodes.")
        if edges[["source", "target"]].isnull().any().any():
            raise ValueError("Source and target nodes must not be null.")
        if edges["sign"].isnull().any():
            raise ValueError("Edge signs must not be null.")
       
    def __repr__(self):
        """
        Generates a developer-centric, informative string representation of the network instance.

        Returns:
            str: A formatted string detailing the network's directionality type, 
                total node density, and total edge count.
        """
        return (
            f"SignedNetwork("
            f"directed={self.directed}, "
            f"nodes={self.number_of_nodes}, "
            f"edges={self.number_of_edges})"
        )
        
    @property
    def directed(self):
        """
        Exposes the directional state configuration of the network topology.

        Returns:
            bool: True if relationships are evaluated as directed arcs; False if undirected.
        """
        return self._directed

    @property
    def edges(self) -> pd.DataFrame:
        """
        Returns a defensive deep copy of the structural network edge list DataFrame.

        Protects internal topological states from external, unintended manipulations at 
        the application layer while preserving full column access for calculations.

        Returns:
            pd.DataFrame: A separate DataFrame instance containing 'source', 'target', and 'sign'.
        """
        return self._edges.copy()  # makes a copy of the edge list so that unwanted manipulation does not happen (if the application is too slow, this needs to be changed)
    
    @property
    def nodes(self) -> tuple:
        """
        Returns an unchangeable, sorted immutable sequence of all unique node identifiers.

        Guarantees a highly reliable, deterministic ordering across subsequent array alignments 
        and matrix factory instantiations.

        Returns:
            tuple: An immutable ordered tuple containing all unique node labels.
        """
        return tuple(self._nodes_list)

    @property
    def number_of_nodes(self) -> int:
        """
        Calculates the overall volume of distinct entities present in the topology.

        Returns:
            int: The total count of unique node keys.
        """
        return len(self._nodes_set)

    @property
    def number_of_edges(self) -> int:
        """
        Calculates the total density of logged signed interactions inside the data array.

        Returns:
            int: The total row count within the underlying edge list.
        """
        return len(self._edges)
    
    def has_node(self, node: Any) -> bool:
        """
        Performs a highly optimized O(1) membership test to verify a node's presence.

        Args:
            node (Any): The unique label identifier of the target node to query.

        Returns:
            bool: True if the node is actively registered within the network topology; otherwise False.
        """
        return node in self._nodes_set
    
    def copy(self):
        """
        Generates a detached duplicate instance of the current signed network topology.

        Creates distinct copies of both the underlying edge arrays and the node registries 
        to guarantee completely separate execution environments for experimental mutations.

        Returns:
            SignedNetwork: A freshly instantiated duplicate network object mirroring 
                the active state.
        """
        return SignedNetwork(
            self._edges.copy(),
            nodes=list(self._nodes_set),
            directed=self._directed
        )
