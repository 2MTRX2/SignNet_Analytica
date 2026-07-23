# CorrelationStrategy.py

from abc import ABC, abstractmethod
import pandas as pd

class CorrelationStrategy(ABC):
    @abstractmethod
    def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
        pass