# RepresentationNormaliser
from abc import ABC, abstractmethod
import pandas as pd

from .NetworkData import NetworkData

class RepresentationNormaliser(ABC):
    """Abstract base class for data representation normalisers.

    This class serves as an interface for all normalization strategies that 
    transform structural data variations (such as adjacency matrices or 
    non-standard edge lists) into the framework's canonical edge list format.
    """

    @abstractmethod
    def to_network_data(self, df: pd.DataFrame) -> NetworkData:
        """Transforms a raw input DataFrame into a standardized edge list format.

        This method must be overridden by any concrete subclass. The resulting 
        DataFrame must strictly contain the columns 'source', 'target', and 'sign', 
        and should have any zero-entries (non-edges) removed.

        Args:
            df (pd.DataFrame): The raw input DataFrame containing the network data 
                in its original structural format.

        Returns:
            pd.DataFrame: A standardized flat edge list DataFrame with exactly 
                three columns: 'source', 'target', and 'sign'.
        """
        pass