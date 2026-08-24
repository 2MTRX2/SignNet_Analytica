# test_CentralityAnalysis.py
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.models.SignedNetwork import SignedNetwork
from signnet.analysis.centrality.centrality_measures.SignedDegreeCentrality import SignedDegreeCentrality
from signnet.analysis.centrality.centrality_measures.PnCentrality import PnCentrality
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBloch import KbCentralityBloch

# =====================================================================
# 1. COMPUTATION TESTS (compute)
# =====================================================================

def test_compute_different_measures(): 
    # ARRANGE
    centrality_measures = [
        MagicMock(spec=SignedDegreeCentrality), 
        MagicMock(spec=PnCentrality),
        MagicMock(spec=KbCentralityBloch)
    ]

    sd_result_df = pd.DataFrame({"Signed Degree (β=1.0)": [1.0, 0.0]}, index=["A", "B"])
    centrality_measures[0].compute.return_value = sd_result_df

    pn_result_df = pd.DataFrame({"PN": [2.0, 2.0]}, index=["A", "B"])
    centrality_measures[1].compute.return_value = pn_result_df

    kb_bloch_result_df = pd.DataFrame({"K-B (Bloch)": [0.5, 0.5]}, index=["A", "B"])

    centrality_measures[2].compute.return_value = kb_bloch_result_df
    mock_network = MagicMock(spec=SignedNetwork)
    
    centrality_analysis = CentralityAnalysis(centrality_measures)

    expected_df = pd.concat([sd_result_df, pn_result_df, kb_bloch_result_df])

    # ACT 
    result_df = centrality_analysis.compute(mock_network)

    # ASSERT
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    centrality_measures[0].compute.assert_called_once_with(mock_network)
    centrality_measures[1].compute.assert_called_once_with(mock_network)
    centrality_measures[2].compute.assert_called_once_with(mock_network)

    result_df = result_df.sort_index()
    expected_df = expected_df.sort_index()
    pd.testing.assert_frame_equal(result_df, expected_df)

    