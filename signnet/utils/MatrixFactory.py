# MatrixFactory.py
import numpy as np

from signnet.models.SignedNetwork import SignedNetwork

class MatrixFactory:
    """
    Factory for generating standardized NumPy matrix representations from structural SignedNetwork instances.

    Consolidates the mathematical transformation pipelines required for advanced matrix operations, 
    such as Katz-Bonacich or PN-centrality computations. All generated matrices strictly 
    adhere to the canonical node ordering defined within the network topology, ensuring absolute 
    compatibility and alignment when aligning matrices across different network measures.
    """

    @staticmethod
    def adjacency(network: SignedNetwork) -> np.ndarray:
        """
        Returns the signed adjacency matrix.

        Entries:
            +1 : positive edge
            -1 : negative edge
             0 : no edge

        Args:
            network (SignedNetwork): The fully initialized network containing the nodes 
                and signed edges to mathematically represent.

        Returns:
            np.ndarray: A square NxN float matrix representing the complete bidirectional 
                signed topology.
        """
        return MatrixFactory._build_matrix(
            network,
            positive_value=1.0,
            negative_value=-1.0
        )

    @staticmethod
    def positive(network: SignedNetwork) -> np.ndarray:
        """
        Returns the positive adjacency matrix A⁺.

        Entries:
                    +1 : positive edge
                     0 : negative edge
                     0 : no edge
        
        Args:
            network (SignedNetwork): The fully initialized network containing the nodes 
                and signed edges to mathematically represent.
        
        Returns:
            np.ndarray: A square NxN float matrix representing the complete bidirectional 
                signed topology.
        """

        return MatrixFactory._build_matrix(
            network,
            positive_value=1.0,
            negative_value=0.0
        )

    @staticmethod
    def negative(network: SignedNetwork) -> np.ndarray:
        """
        Returns the negative adjacency matrix A⁻.
        
        Entries:
                     0 : positive edge
                     1 : negative edge
                     0 : no edge
                
        Args:
            network (SignedNetwork): The fully initialized network containing the nodes 
                and signed edges to mathematically represent.
                
        Returns:
            np.ndarray: A square NxN float matrix representing the complete bidirectional 
                signed topology.
        """

        return MatrixFactory._build_matrix(
            network,
            positive_value=0.0,
            negative_value=1.0
        )

    @staticmethod
    def tilde(network: SignedNetwork) -> np.ndarray:
        """Returns the transformed matrix

            Ã = A⁺ − 2A⁻

        used for PN-centrality.
        """

        return MatrixFactory._build_matrix(
            network,
            positive_value=1.0,
            negative_value=-2.0
        )

    @staticmethod
    def _build_matrix(
        network: SignedNetwork,
        positive_value: float,
        negative_value: float,
    ) -> np.ndarray:
        """
        Internal foundational builder that maps structural network edges onto a dense NumPy matrix.

        Instantiates a zero-filled float matrix based on the net node count and builds a localized 
        index dictionary lookup to guarantee proper node coordinate mapping. It iterates sequentially 
        through the structural edge list tuples, scales coordinates on the basis of edge signs, and 
        mirrors entries along the main diagonal if the underlying network topology is undirected.

        Args:
            network (SignedNetwork): The fully initialized network containing the nodes 
                and signed edges to mathematically represent.
            positive_value (float): The specific weight value to inject for a structurally 
                positive edge.
            negative_value (float): The specific weight value to inject for a structurally 
                negative edge.

        Returns:
            np.ndarray: A dense square 2D matrix populated according to the provided parameter 
                scaling rules.
        """

        nodes = network.nodes
        n = network.number_of_nodes

        # create a mapping between nodes and matrix indices (0 to N-1)
        node_to_idx = {
            node: idx
            for idx, node in enumerate(nodes)
        }

        # create the signed adjency matrix filled with 0s
        matrix = np.zeros((n, n), dtype=float)

        # get all the edges of the network
        for source, target, sign in network.edges.itertuples(index=False):

            # get the index of each node
            i = node_to_idx[source]
            j = node_to_idx[target]

            # assgin the appropriate value
            if sign > 0:
                value = positive_value
            elif sign < 0:
                value = negative_value
            else:
                continue

            matrix[i, j] = value

            # mirror if not directed
            if not network.directed:
                matrix[j, i] = value

        return matrix