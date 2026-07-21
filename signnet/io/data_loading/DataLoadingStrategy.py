# DataLoadingStrategy.py
from abc import ABC, abstractmethod
import pandas as pd

from signnet.io.data_representation.NetworkData import NetworkData


class DataLoadingStrategy(ABC):
    """Abstract base class for data loading strategies within the research framework.
    This class serves as an interface for all components responsible for 
    reading signed social network data from various file formats or data sources. 
    """

    @abstractmethod
    def read_raw(self, file_source) -> pd.DataFrame:
        """Loads data from the given source and returns a pandas dataframe.

        Args:
            file_source: Path to the file, URL, or a file-like object.

        Returns:
            NetworkData: The loaded data.
        """
        pass

    @abstractmethod
    def load(self, file_source) -> NetworkData:
        """Loads data from the given source and returns a NetworkData class.

        Args:
            file_source: Path to the file, URL, or a file-like object.

        Returns:
            NetworkData: The loaded data.
        """
        pass