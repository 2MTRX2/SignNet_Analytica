#EdgeListNormaliser
    
import pandas as pd

from .RepresentationNormaliser import RepresentationNormaliser
from .NetworkData import NetworkData


class EdgeListNormaliser(RepresentationNormaliser):
    """Normalizes an existing edge list DataFrame into the framework's canonical format.

    This strategy handles data that is already structured as a list of edges but 
    might use non-standard column names. It maps and renames the custom columns 
    to the uniform 'source', 'target', and 'sign' format required by the pipeline.
    """

    def __init__(self, source_col: str = 'source', target_col: str = 'target', sign_col: str = 'sign'):
        """Initializes the EdgeListRepresentation with custom column mappings.

        Args:
            source_col (str): The name of the column representing the origin node.
            target_col (str): The name of the column representing the destination node.
            sign_col (str): The name of the column representing the edge sign/weight.
        """
        self.source_col = source_col
        self.target_col = target_col
        self.sign_col = sign_col

    def to_network_data(self, df: pd.DataFrame) -> NetworkData:
        """Renames and structures the DataFrame columns to match the framework's standard.

        Args:
            df (pd.DataFrame): The raw input DataFrame containing the edge list.

        Returns:
            pd.DataFrame: A cleaned DataFrame with exactly three columns: 
                'source', 'target', and 'sign', with any zero-entries filtered out.
        """
        # Create a copy to prevent modifying the original DataFrame in-place
        cleaned_df = df.copy()

        # Select and reorder only the relevant columns based on the mapping
        cleaned_df = cleaned_df[[self.source_col, self.target_col, self.sign_col]]

        # Rename columns to the framework's canonical names
        cleaned_df.columns = ['source', 'target', 'sign']

        # Filter out non-existent relationships (sign == 0), identical to the Matrix strategy
        cleaned_df = cleaned_df[cleaned_df['sign'] != 0].reset_index(drop=True)

        return NetworkData(edges=cleaned_df, nodes=None)
