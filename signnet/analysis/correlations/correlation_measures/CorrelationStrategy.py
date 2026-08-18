# CorrelationStrategy.py
from abc import ABC, abstractmethod
import pandas as pd

class CorrelationStrategy(ABC):
    """
    Abstract base class establishing the behavioral interface for statistical correlation strategies.

    Defines the structural contract for implementing pairwise correlation algorithms within 
    the framework. By utilizing the Strategy Pattern, this component decouples the analytical 
    orchestration layers from concrete mathematical computations, allowing new metric evaluators 
    (e.g., Pearson, Spearman, Kendall) to be injected interchangeably at runtime.
    """
    @abstractmethod
    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        """
        Abstract method to calculate the correlation coefficient and its corresponding p-value.

        Must be overridden by concrete strategy implementations to ingest two parallel, aligned 
        data sequences and perform the specialized statistical test over their shared observations.

        Args:
            x (pd.Series): The first continuous or ordinal variable sequence for the pairwise comparison.
            y (pd.Series): The second continuous or ordinal variable sequence, aligned element-by-element 
                with the first sequence.

        Returns:
            tuple[float, float]: A tuple containing exactly two elements:
                - The calculated correlation coefficient (typically bounded between -1.0 and 1.0).
                - The asymptotic or exact two-tailed p-value representing the statistical significance.
        """
        pass