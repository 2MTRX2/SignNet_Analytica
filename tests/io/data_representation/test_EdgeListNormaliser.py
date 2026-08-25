# test_EdgeListNormaliser.py
import pandas as pd

from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_representation.NetworkData import NetworkData

# =====================================================================
# 1. TRANSFORM
# =====================================================================

def test_to_network_data_with_default_columns():
    # ARRANGE
    normaliser = EdgeListNormaliser()
    
    # standard names for columns
    raw_df = pd.DataFrame({
        "source": ["A", "A", "B"],
        "target": ["B", "C", "C"],
        "sign": [1, -1, 0]
    })

    # expected only colmuns with non-zero entries
    expected_edges = pd.DataFrame({
        "source": ["A", "A"],
        "target": ["B", "C"],
        "sign": [1, -1]
    }).reset_index(drop=True)

    # ACT
    network_data = normaliser.to_network_data(raw_df)

    # ASSERT
    assert isinstance(network_data, NetworkData)
    pd.testing.assert_frame_equal(network_data.edges, expected_edges)
    assert network_data.nodes is None


def test_to_network_data_with_custom_columns():
    # ARRANGE
    normaliser = EdgeListNormaliser(
        source_col="from", 
        target_col="to", 
        sign_col="weight"
    )
    
    raw_df = pd.DataFrame({
        "from": ["X", "Y"],
        "info": ["ignore_me", "ignore_me_too"],
        "to": ["Y", "Z"],
        "weight": [1, 1]
    })

    expected_edges = pd.DataFrame({
        "source": ["X", "Y"],
        "target": ["Y", "Z"],
        "sign": [1, 1]
    })

    # ACT
    network_data = normaliser.to_network_data(raw_df)

    # ASSERT
    pd.testing.assert_frame_equal(network_data.edges, expected_edges)


def test_to_network_data_cleans_column_whitespace_and_bom():
    # ARRANGE
    normaliser = EdgeListNormaliser(source_col="source", target_col="target", sign_col="sign")
    
    # column names with white spaces
    raw_df = pd.DataFrame({
        "\ufeffsource": ["A"],
        " target ": ["B"],
        "sign": [1]
    })

    expected_edges = pd.DataFrame({
        "source": ["A"],
        "target": ["B"],
        "sign": [1]
    })

    # ACT
    network_data = normaliser.to_network_data(raw_df)

    # ASSERT
    pd.testing.assert_frame_equal(network_data.edges, expected_edges)


def test_to_network_data_does_not_modify_original_dataframe():
    # ARRANGE
    normaliser = EdgeListNormaliser()
    raw_df = pd.DataFrame({
        "source": ["A", "B"],
        "target": ["B", "C"],
        "sign": [1, 0] 
    })
    
    original_df_backup = raw_df.copy()

    # ACT
    _ = normaliser.to_network_data(raw_df)

    # ASSERT
    pd.testing.assert_frame_equal(raw_df, original_df_backup)