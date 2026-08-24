# test_SpearmanStrategy.py
import pandas as pd
from scipy.stats import spearmanr
import pytest

from signnet.analysis.correlations.correlation_measures.SpearmanStrategy import SpearmanStrategy


# =====================================================================
# 1. COMPUTATION TESTS (calculate)
# =====================================================================

def test_calculate_spearman(): 
    # ARRANGE
    spearman_corr = SpearmanStrategy()

    series_x = pd.Series([1, 2, 3])
    series_y = pd.Series([2, 4, 6])

    expected_coeff, expected_p_val = spearmanr(series_x, series_y)
    expected_coeff, expected_p_val = float(expected_coeff), float(expected_p_val)

    # ACT
    results_coeff, results_p_val = spearman_corr.calculate(series_x, series_y)

    # ASSERT
    assert isinstance(results_coeff, float)
    assert isinstance(results_p_val, float)

    assert results_coeff == pytest.approx(expected_coeff)
    assert results_p_val == pytest.approx(expected_p_val)