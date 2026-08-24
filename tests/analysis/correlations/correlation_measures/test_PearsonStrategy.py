# test_PearsonStrategy.py
import pandas as pd
from scipy.stats import pearsonr
import pytest

from signnet.analysis.correlations.correlation_measures.PearsonStrategy import PearsonStrategy


# =====================================================================
# 1. COMPUTATION TESTS (calculate)
# =====================================================================

def test_calculate_pearson(): 
    # ARRANGE
    pearson_corr = PearsonStrategy()

    series_x = pd.Series([1, 2, 3])
    series_y = pd.Series([2, 4, 6])

    expected_coeff, expected_p_val = pearsonr(series_x, series_y)
    expected_coeff, expected_p_val = float(expected_coeff), float(expected_p_val)

    # ACT
    results_coeff, results_p_val = pearson_corr.calculate(series_x, series_y)

    # ASSERT
    assert isinstance(results_coeff, float)
    assert isinstance(results_p_val, float)

    assert results_coeff == pytest.approx(expected_coeff)
    assert results_p_val == pytest.approx(expected_p_val)