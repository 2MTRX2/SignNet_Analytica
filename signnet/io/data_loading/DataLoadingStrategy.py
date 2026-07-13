# DataLoadingStrategy.py
from abc import ABC, abstractmethod
import pandas as pd


class DataLoadingStrategy(ABC):
    """Abstract base class for data loading strategies within the research framework.
    This class serves as an interface for all components responsible for 
    reading signed social network data from various file formats or data sources. 
    """

    @abstractmethod
    def load(self, file_source) -> pd.DataFrame:
        """Loads data from the given source and returns a pandas DataFrame.

        Args:
            file_source: Path to the file, URL, or a file-like object.

        Returns:
            pd.DataFrame: The loaded data.
        """
        pass