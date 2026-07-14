# matrix_helpers.py
import pandas as pd

def transform_matrix_to_edgelist(
    matrix_df: pd.DataFrame, 
    source_col: str = 'source', 
    target_col: str = 'target', 
    sign_col: str = 'sign'
) -> pd.DataFrame:
    """Transforms a square adjacency matrix into a standardized flat edge list.

    This utility function converts a 2D network representation (Wide-Format) 
    into a 1D relational table (Long-Format). It validates the input structure,
    removes all non-existent edges (zero entries), and formats the columns.

    Args:
        matrix_df (pd.DataFrame): The input square adjacency matrix where both 
            index and columns represent the matching node labels.
        source_col (str, optional): The name for the resulting origin node column. 
            Defaults to 'source'.
        target_col (str, optional): The name for the resulting destination node column. 
            Defaults to 'target'.
        sign_col (str, optional): The name for the resulting edge sign/weight column. 
            Defaults to 'sign'.

    Returns:
        pd.DataFrame: A cleaned flat DataFrame with exactly three columns 
            representing the active signed relationships.

    Raises:
        ValueError: If the input DataFrame is not a square matrix (number of rows 
            does not equal the number of columns).
    """
    # Check if the adjacency matrix is mathematically square
    if matrix_df.shape[0] != matrix_df.shape[1]:
        raise ValueError("The provided adjacency matrix must be square (NxN).")
    
    # Transform the 2D matrix into a 1D multi-index series
    edgelist_df = matrix_df.stack().reset_index()
    
    # Rename columns to the framework's canonical names
    edgelist_df.columns = [source_col, target_col, sign_col]
    
    # Filter out all lines where no edge exists (sign == 0) and clean the row index
    edgelist_df = edgelist_df[edgelist_df[sign_col] != 0].reset_index(drop=True)
    
    return edgelist_df
