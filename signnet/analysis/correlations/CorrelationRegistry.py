# CorrelationRegistry.py
from typing import Type

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy
from signnet.analysis.correlations.correlation_measures.KendallStrategy import KendallStrategy
from signnet.analysis.correlations.correlation_measures.PearsonStrategy import PearsonStrategy
from signnet.analysis.correlations.correlation_measures.SpearmanStrategy import SpearmanStrategy

class CorrelationRegistry: 
    _REGISTRY: dict[str, Type[CorrelationStrategy]] = {
            "Spearman Rank Correlation (Recommended)": SpearmanStrategy,
            "Pearson Linear Correlation": PearsonStrategy,
            "Kendall Tau Correlation": KendallStrategy,
        }
    
    @classmethod
    def get_available_names(cls) -> list[str]:
        """Returns all registred names of correlation measures."""
        return list(cls._REGISTRY.keys())
    
    @classmethod
    def get_measure_class(cls, name: str) -> Type[CorrelationStrategy]:
        """Returns the uninitialised correlation measure class for a specific name."""
        if name not in cls._REGISTRY:
            raise ValueError(f"Centrality measure '{name}' is not registered.")
        return cls._REGISTRY[name]