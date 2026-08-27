# test_CorrelationAnalysis
import pytest
import pandas as pd
import numpy as np

from signnet.analysis.correlations.CorrelationAnalysis import CorrelationAnalysis
from signnet.analysis.correlations.correlation_measures.KendallStrategy import KendallStrategy
from signnet.analysis.correlations.correlation_measures.PearsonStrategy import PearsonStrategy
from signnet.analysis.correlations.correlation_measures.SpearmanStrategy import SpearmanStrategy

# =====================================================================
# 1. ANALYSIS TESTS
# =====================================================================

@pytest.mark.parametrize("correlation_strategy", [
    KendallStrategy(),
    PearsonStrategy(),
    SpearmanStrategy()
])
def test_analyse_corr_with_no_index_column(correlation_strategy, monkeypatch): 
    # ARRANGE
    monkeypatch.setattr(correlation_strategy, "calculate", lambda x, y: (1.0, 0.0))
    corr_analysis = CorrelationAnalysis(correlation_strategy)

    centrality_measures = pd.DataFrame({
        "centrality_measure_1": [2, 3], 
        "centrality_measure_2": [4, 5]
    })

    cols = ["centrality_measure_1", "centrality_measure_2"]
    expected_corr_df = pd.DataFrame([[1.0, 1.0], [1.0, 1.0]], index=cols, columns=cols)
    expected_p_val_df = pd.DataFrame([[0.0, 0.0], [0.0, 0.0]], index=cols, columns=cols)

    # ACT
    result_corr_df, result_p_val_df = corr_analysis.analyze_correlations(centrality_measures)

    # ASSERT
    assert isinstance(result_corr_df, pd.DataFrame)
    assert isinstance(result_p_val_df, pd.DataFrame)  
    assert not result_corr_df.empty
    assert not result_p_val_df.empty

    result_corr_df = result_corr_df.sort_index()
    result_p_val_df = result_p_val_df.sort_index()
    expected_corr_df = expected_corr_df.sort_index()
    expected_p_val_df = expected_p_val_df.sort_index()

    pd.testing.assert_frame_equal(result_corr_df, expected_corr_df)
    pd.testing.assert_frame_equal(result_p_val_df, expected_p_val_df)


@pytest.mark.parametrize("correlation_strategy", [
    KendallStrategy(),
    PearsonStrategy(),
    SpearmanStrategy()
])
def test_analyse_corr_without_any_numbers(correlation_strategy): 
    # ARRANGE
    corr_analysis = CorrelationAnalysis(correlation_strategy)

    centrality_measures = pd.DataFrame({
        "node": ["A", "B"],
        "centrality_measure_1": ["a", "b"], 
        "centrality_measure_2": ["a", "b"]
    })

    # ACT
    result_corr_df, result_p_val_df = corr_analysis.analyze_correlations(centrality_measures)

    # ASSERT
    assert result_corr_df.empty
    assert result_p_val_df.empty


@pytest.mark.parametrize("correlation_strategy", [
    KendallStrategy(),
    PearsonStrategy(),
    SpearmanStrategy()
])
def test_analyse_corr(correlation_strategy, monkeypatch): 
    # ARRANGE
    monkeypatch.setattr(correlation_strategy, "calculate", lambda x, y: (0.8, 0.05))
    corr_analysis = CorrelationAnalysis(correlation_strategy)

    centrality_measures = pd.DataFrame({
        "node": ["A", "B"],
        "centrality_measure_1": [2, 3], 
        "centrality_measure_2": [4, 5]
    })

    cols = ["centrality_measure_1", "centrality_measure_2"]
    expected_corr_df = pd.DataFrame([[1.0, 0.8], [0.8, 1.0]], index=cols, columns=cols)
    expected_p_val_df = pd.DataFrame([[0.0, 0.05], [0.05, 0.00]], index=cols, columns=cols)

    # ACT
    result_corr_df, result_p_val_df = corr_analysis.analyze_correlations(centrality_measures)

    # ASSERT
    assert isinstance(result_corr_df, pd.DataFrame)
    assert isinstance(result_p_val_df, pd.DataFrame)  
    assert not result_corr_df.empty
    assert not result_p_val_df.empty

    result_corr_df = result_corr_df.sort_index()
    result_p_val_df = result_p_val_df.sort_index()
    expected_corr_df = expected_corr_df.sort_index()
    expected_p_val_df = expected_p_val_df.sort_index()

    pd.testing.assert_frame_equal(result_corr_df, expected_corr_df)
    pd.testing.assert_frame_equal(result_p_val_df, expected_p_val_df)
