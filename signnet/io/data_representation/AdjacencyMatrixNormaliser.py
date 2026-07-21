# AdjacencyMatrixNormaliser
import pandas as pd

from signnet.io.data_representation.RepresentationNormaliser import RepresentationNormaliser
from signnet.utils.matrix_helpers import transform_matrix_to_edgelist
from signnet.io.data_representation.NetworkData import NetworkData

class AdjacencyMatrixNormaliser(RepresentationNormaliser):
    """Normalizes an adjacency matrix into the framework's canonical node & edge list.

    Expected input format:
    - The first column contains the row node labels.
    - The subsequent columns contain the column node labels as headers.
    - Row and column labels must match in order and naming.
    - Matrix values represent edge signs (+1, -1) or weights.
    - A value of 0 indicates that no edge exists.
    """

    def to_network_data(self, df) -> NetworkData:
        """Transforms a raw adjacency matrix DataFrame into a standardized node & edge list.

        Args:
            df (pd.DataFrame): The raw DataFrame containing the matrix data, 
                where the first column holds the row labels.

        Returns:
            pd.DataFrame: A standardized flat edge list DataFrame with 
                'source', 'target', and 'sign' columns.
        """
        matrix = df.set_index(df.columns[0])
        all_nodes = list(matrix.index)
        # deletes the first index column also in the header
        matrix = matrix[all_nodes] 
        edges_df = transform_matrix_to_edgelist(matrix)

        return NetworkData(edges=edges_df, nodes=all_nodes)