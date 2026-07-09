# RepresentationStrategy.py
from abc import ABC, abstractmethod
import pandas as pd

class RepresentationStrategy(ABC):

    @abstractmethod
    def transform(self, df) -> pd.DataFrame:
        pass