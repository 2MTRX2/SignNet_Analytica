# ExcelStrategy.py
import pandas as pd

from .DataLoadingStrategy import DataLoadingStrategy
from io.data_representation.RepresentationNormaliser import RepresentationNormaliser

class ExcelStrategy(DataLoadingStrategy):
    """Concrete data loading strategy for Excel files (.xlsx, .xls).

    This class handles the File I/O for Excel data and delegates the structural 
    transformation to a dedicated representation handler.

    Attributes:
        representation: An object or strategy responsible for transforming the 
            loaded DataFrame into a standardized edge list format.
    """

    def __init__(self, representation: RepresentationNormaliser):
        """Initializes the ExcelStrategy with a specific data representation handler.

        Args:
            representation: The structural representation handler that implements 
                the `to_edge_list(df)` method.
        """
        self.representation = representation

    def load(self, file_source) -> pd.DataFrame:
        """Loads an Excel file and converts it into a standardized edge list DataFrame.

        This method reads the Excel sheet into a raw pandas DataFrame and passes it 
        to the representation handler. To ensure compatibility with both edge lists 
        and matrices, the file is read without hardcoded index columns.

        Args:
            file_source (str or file-like object): The path to the Excel file or 
                a file-like object (such as a Streamlit upload stream).

        Returns:
            pd.DataFrame: A standardized flat edge list DataFrame containing 
                the network connections and their respective signs.
        """

        df = pd.read_excel(file_source)

        return self.representation.to_network_data(df)
