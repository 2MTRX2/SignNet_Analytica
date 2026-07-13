# MatrixFactory.py

import numpy as np

from models.SignedNetwork import SignedNetwork


class MatrixFactory:
    """Factory for creating matrix representations of a SignedNetwork.

    All matrices follow the node ordering defined by
    `SignedNetwork.nodes`, ensuring that every matrix representation
    is compatible across different centrality measures.
    """

    @staticmethod
    def adjacency(network: SignedNetwork) -> np.ndarray:
        """Returns the signed adjacency matrix.

        Entries:
            +1 : positive edge
            -1 : negative edge
             0 : no edge
        """
        return MatrixFactory._build_matrix(
            network,
            positive_value=1.0,
            negative_value=-1.0
        )

    @staticmethod
    def positive(network: SignedNetwork) -> np.ndarray:
        """Returns the positive adjacency matrix A⁺."""

        return MatrixFactory._build_matrix(
            network,
            positive_value=1.0,
            negative_value=0.0
        )

    @staticmethod
    def negative(network: SignedNetwork) -> np.ndarray:
        """Returns the negative adjacency matrix A⁻."""

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
        """Internal helper for constructing adjacency-like matrices."""

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

            i = node_to_idx[source]
            j = node_to_idx[target]

            if sign > 0:
                value = positive_value
            elif sign < 0:
                value = negative_value
            else:
                continue

            matrix[i, j] = value

            if not network.directed:
                matrix[j, i] = value

        return matrix