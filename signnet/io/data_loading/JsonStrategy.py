import pandas as pd

from signnet.io.data_loading.DataLoadingStrategy import DataLoadingStrategy
from signnet.io.data_representation.RepresentationNormaliser import RepresentationNormaliser

class JsonStrategy(DataLoadingStrategy):
    """Concrete data loading strategy for JSON files.

    This class handles the File I/O for JSON data. Since JSON structures can 
    vary heavily, it reads the data raw and delegates the parsing and structural 
    transformation to a dedicated representation handler.

    Attributes:
        representation: An object or strategy responsible for transforming the 
            loaded DataFrame into a standardized edge list format.
    """

    def __init__(self, representation: RepresentationNormaliser):
        """Initializes the JsonStrategy with a specific data representation handler.

        Args:
            representation: The structural representation handler that implements 
                the `to_edge_list(df)` method.
        """
        self.representation = representation

    def load(self, file_source) -> pd.DataFrame:
        """Loads a JSON file and converts it into a standardized edge list DataFrame.

        This method reads the JSON input into a raw pandas DataFrame. It does 
        not enforce an index column directly, leaving the structural decoding 
        (e.g., orientation parsing) to the representation handler.

        Args:
            file_source (str or file-like object): The path to the JSON file or 
                a file-like object (such as a Streamlit upload stream).

        Returns:
            pd.DataFrame: A standardized flat edge list DataFrame containing 
                the network connections and their respective signs.
        """
        df = pd.read_json(file_source)

        return self.representation.to_network_data(df)
