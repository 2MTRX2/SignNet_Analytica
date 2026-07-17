# CentralityAnalysis.py
import pandas as pd

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.models.SignedNetwork import SignedNetwork


class CentralityAnalysis:

    def __init__(self, measures: list[CentralityMeasure]):
        self._measures = measures

    def compute(self, network: SignedNetwork) -> pd.DataFrame:

        results = []

        for measure in self._measures:
            results.append(
                measure.compute(network)
            )

        return pd.concat(results, axis=1)