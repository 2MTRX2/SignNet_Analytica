# DataLoadingStrategy.py
from abc import ABC, abstractmethod
import pandas as pd


class DataLoadingStrategy(ABC):
    """Abstract base class for data loading strategies within the research framework.
    This class serves as an interface for all components responsible for 
    reading signed social network data from various file formats or data sources. 
    """

    # loads data and returns a pandas dataframe
    @abstractmethod
    def load(self, file_source) -> pd.DataFrame:
        pass