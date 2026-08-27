# test_matrix_to_edgelist.py
import numpy as np
import pandas as pd
import pytest

from signnet.utils.matrix_to_edgelist import transform_matrix_to_edgelist

# =====================================================================
# MATRIX TO EDGELIST TRANSFORMATION TESTS
# =====================================================================

def test_transform_matrix_to_edgelist_undirected_flow():
    # ARRANGE 
    matrix_data = [
        [0,  1, -1],
        [1, 0, 0],  
        [-1, 0, 0] 
    ]
    nodes = ["A", "B", "C"]
    matrix_df = pd.DataFrame(matrix_data, index=nodes, columns=nodes)

    # ACT
    result = transform_matrix_to_edgelist(matrix_df, directed=False)

    # ASSERT 
    expected_df = pd.DataFrame({
        'source': ['A', 'A'],
        'target': ['B', 'C'],
        'sign': [1.0, -1.0]
    })

    pd.testing.assert_frame_equal(result, expected_df)


def test_transform_matrix_to_edgelist_directed_flow():
    # ARRANGE 
    matrix_data = [
        [0, 1, 0], 
        [-1, 0, 0], 
        [0, 0, 0]
    ]
    nodes = ["A", "B", "C"]
    matrix_df = pd.DataFrame(matrix_data, index=nodes, columns=nodes)

    # ACT
    result = transform_matrix_to_edgelist(matrix_df, directed=True)

    # ASSERT 
    expected_df = pd.DataFrame({
        'source': ['A', 'B'],
        'target': ['B', 'A'],
        'sign': [1.0, -1.0]
    })

    pd.testing.assert_frame_equal(result, expected_df)


def test_transform_matrix_to_edgelist_custom_column_names():
    # ARRANGE 
    matrix_data = [[0, 1], [1, 0]]
    nodes = ["A", "B"]
    matrix_df = pd.DataFrame(matrix_data, index=nodes, columns=nodes)

    # ACT -
    result = transform_matrix_to_edgelist(
        matrix_df, 
        directed=False,
        source_col="from", 
        target_col="to", 
        sign_col="weight"
    )

    # ASSERT 
    assert result.columns.tolist() == ["from", "to", "weight"]
    assert result.loc[0, "from"] == "A"
    assert result.loc[0, "to"] == "B"
    assert result.loc[0, "weight"] == 1.0


def test_transform_matrix_to_edgelist_non_numeric_handling():
    # ARRANGE 
    matrix_data = [
        [0, "1", "invalid_string"],
        [-1, 0, np.nan],
        ["-1", 0, 0]
    ]
    nodes = ["A", "B", "C"]
    matrix_df = pd.DataFrame(matrix_data, index=nodes, columns=nodes)

    # ACT
    result = transform_matrix_to_edgelist(matrix_df, directed=True)

    # ASSERT 
    expected_df = pd.DataFrame({
        'source': ['A', 'B', 'C'],
        'target': ['B', 'A', 'A'],
        'sign': [1.0, -1.0, -1.0]
    })

    pd.testing.assert_frame_equal(result, expected_df)


def test_transform_matrix_to_edgelist_not_square_raises_error():
    # ARRANGE 
    matrix_data = [
        [0, 1],
        [1, 0],
        [-1, 1]
    ]
    matrix_df = pd.DataFrame(matrix_data, index=["A", "B", "C"], columns=["A", "B"])

    # ACT & ASSERT 
    with pytest.raises(ValueError, match="The provided adjacency matrix must be square"):
        transform_matrix_to_edgelist(matrix_df)
