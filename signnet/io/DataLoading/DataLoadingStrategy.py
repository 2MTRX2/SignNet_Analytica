# DataLoadingStrategy.py
from abc import ABC, abstractmethod
import pandas as pd


class DataLoadingStrategy(ABC):

    # loads data and returns a pandas dataframe
    @abstractmethod
    def load(self, file_source) -> pd.DataFrame:
        pass