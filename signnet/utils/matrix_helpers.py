# utils.py
import pandas as pd

def transform_matrix_to_edgelist(matrix_df: pd.DataFrame, source_col: str = 'source', target_col: str = 'target', sign_col: str = 'sign') -> pd.DataFrame:
    """
    Transforms a quadradic adjency matrix (Wide-Format) into a flat list
    of edges (Long-Format) and removes all zero-entries.
    """
    # check if it is a quadratic adjency matrix
    if matrix_df.shape[0] != matrix_df.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
    
    # Transform the maxtrix into a list
    edgelist_df = matrix_df.stack().reset_index()
    
    # rename columns
    edgelist_df.columns = [source_col, target_col, sign_col]
    
    # remove all zero-entries
    edgelist_df = edgelist_df[edgelist_df[sign_col] != 0].reset_index(drop=True)
    
    return edgelist_df