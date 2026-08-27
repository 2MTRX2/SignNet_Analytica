# test_CentralityResultFormatter.py
import pandas as pd

from signnet.utils.CentralityResultFormatter import CentralityResultFormatter

# =====================================================================
# CENTRALITY RESULT FORMATTER TESTS
# =====================================================================

def test_from_records_standard_flow():
    # ARRANGE
    records = [
        {"node": "A", "metric_1": 0.5, "metric_2": 1.2},
        {"node": "B", "metric_1": -0.2, "metric_2": 3.4},
        {"node": "C", "metric_1": 0.0, "metric_2": 0.1}
    ]
    
    # ACT
    result = CentralityResultFormatter.from_records(records, index_column="node")
    
    # ASSERT
    assert result.index.name == "node"
    assert result.index.tolist() == ["A", "B", "C"]
    assert result.columns.tolist() == ["metric_1", "metric_2"]
    
    expected_df = pd.DataFrame(
        data={"metric_1": [0.5, -0.2, 0.0], "metric_2": [1.2, 3.4, 0.1]},
        index=pd.Index(["A", "B", "C"], name="node")
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_from_records_custom_index_column():
    # ARRANGE 
    records = [
        {"vertex_id": "V1", "score": 10},
        {"vertex_id": "V2", "score": 20}
    ]
    
    # ACT
    result = CentralityResultFormatter.from_records(records, index_column="vertex_id")
    
    # ASSERT
    assert result.index.name == "vertex_id"
    assert result.index.tolist() == ["V1", "V2"]
    assert result.columns.tolist() == ["score"]


def test_from_dict_standard_flow():
    # ARRANGE
    scores_dict = {"A": 0.85, "B": -0.15, "C": 0.0}
    metric_name = "Katz Centrality"
    
    # ACT
    result = CentralityResultFormatter.from_dict(scores_dict, metric_name=metric_name)
    
    # ASSERT
    assert result.index.name == "node"
    assert result.index.tolist() == ["A", "B", "C"]
    assert result.columns.tolist() == ["Katz Centrality"]
    
    expected_df = pd.DataFrame(
        data={"Katz Centrality": [0.85, -0.15, 0.0]},
        index=pd.Index(["A", "B", "C"], name="node")
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_from_array_standard_flow():
    # ARRANGE 
    nodes = ["A", "B", "C"]
    scores = [1.0286, 1.0635, 0.9094]
    metric_name = "Ballester (2006)"
    
    # ACT
    result = CentralityResultFormatter.from_array(nodes, scores, metric_name=metric_name)
    
    # ASSERT
    assert result.index.name == "node"
    assert result.index.tolist() == ["A", "B", "C"]
    assert result.columns.tolist() == ["Ballester (2006)"]
    
    expected_df = pd.DataFrame(
        data={"Ballester (2006)": [1.0286, 1.0635, 0.9094]},
        index=pd.Index(["A", "B", "C"], name="node")
    )
    pd.testing.assert_frame_equal(result, expected_df)


def test_from_array_mismatched_lengths():
    # ARRANGE 
    nodes = ["A", "B"]
    scores = [0.5]  
    metric_name = "PN Centrality"
    
    # ACT
    result = CentralityResultFormatter.from_array(nodes, scores, metric_name=metric_name)
    
    # ASSERT
    assert len(result) == 1
    assert result.index.tolist() == ["A"]
