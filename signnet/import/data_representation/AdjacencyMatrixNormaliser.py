# AdjacencyMatrixNormaliser
import pandas as pd

from .RepresentationNormaliser import RepresentationNormaliser
from signnet.utils.matrix_helpers import transform_matrix_to_edgelist

class AdjacencyMatrixNormaliser(RepresentationNormaliser):
    """Normalizes an adjacency matrix into the framework's canonical edge list.

    Expected input format:
    - The first column contains the row node labels.
    - The subsequent columns contain the column node labels as headers.
    - Row and column labels must match in order and naming.
    - Matrix values represent edge signs (+1, -1) or weights.
    - A value of 0 indicates that no edge exists.
    """

    def to_edge_list(self, df) -> pd.DataFrame:
        """Transforms a raw adjacency matrix DataFrame into a standardized edge list.

        Args:
            df (pd.DataFrame): The raw DataFrame containing the matrix data, 
                where the first column holds the row labels.

        Returns:
            pd.DataFrame: A standardized flat edge list DataFrame with 
                'source', 'target', and 'sign' columns.
        """
        matrix = df.set_index(df.columns[0])
        return transform_matrix_to_edgelist(matrix)