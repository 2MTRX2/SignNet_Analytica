# CentralityRegistry.py
from typing import Type

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.analysis.centrality.centrality_measures.SignedDegreeCentrality import SignedDegreeCentrality
from signnet.analysis.centrality.centrality_measures.PnCentrality import PnCentrality
from signnet.analysis.centrality.centrality_measures.PiiCentrality import PiiCentrality
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBallester import KbCentralityBallester
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBloch import KbCentralityBloch
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralitySadler import KbCentralitySadler

class CentralityRegistry:
    _REGISTRY: dict[str, Type[CentralityMeasure]] = {
        "Signed Degree": SignedDegreeCentrality,
        "PN Centrality": PnCentrality,
        "PII Centrality": PiiCentrality,
        "KB Centrality (Ballester)": KbCentralityBallester,
        "KB Centrality (Bloch)": KbCentralityBloch,
        "KB Centrality (Sadler)": KbCentralitySadler
    }

    @classmethod
    def get_available_names(cls) -> list[str]:
        """Returns all registred names of the different centrality measures."""
        return list(cls._REGISTRY.keys())

    @classmethod
    def get_measure_class(cls, name: str) -> Type[CentralityMeasure]:
        """Returns the uninitialised class for a specific name (centrality measure)."""
        if name not in cls._REGISTRY:
            raise ValueError(f"Centrality measure '{name}' is not registered.")
        return cls._REGISTRY[name]
