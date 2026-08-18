# DatasetRegistry.py
import os
from dataclasses import dataclass

@dataclass
class DatasetInfo:
    """
    Encapsulates the structural and analytical metadata of a predefined network dataset.

    Acts as an immutable data transfer object (DTO) that holds file properties, structural 
    topologies, and contextual metadata necessary for runtime dataset resolution and 
    user-facing documentation.

    Attributes:
        name (str): The canonical, descriptive title of the specific network dataset.
        filename (str): The physical name of the file residing within the framework's data directory.
        representation_type (str): The network format configuration (e.g., 'Adjacency Matrix', 'Edge List').
        file_type (str): The raw storage format extension, typically 'CSV'.
        description (str): A summary outlining the origin, scale, and context of the dataset.
    """
    name: str
    filename: str
    representation_type: str
    file_type: str
    description: str

class DatasetRegistry:
    """
    Registry that manages all predefined datasets in the framework.

    Consolidates the file-system paths and metadata configurations for built-in network 
    benchmarks. It resolves data directory structures relative to the package root and provides 
    unified accessors to fetch, query, and locate raw network files for analysis components.
    """

    # Starting point is our current file DataRegistry.py and we move outside to signnet_programming_python
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Move to the directory data
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # Predefined Datasets
    DATASETS = {
        "Sampson Monks (Time 3)": DatasetInfo(
            name="Sampson Monks (signed, T3)",
            filename="sampson_signed_t3.csv",
            representation_type="Adjacency Matrix",
            file_type="CSV",
            description="Samuel F. Sampson's famous social network dataset from 1968, capturing positive and negative relationships among 18 monks during a monastery crisis (Time 3)."
        ), 
        "Gama Network of Alliances (positive) and Conflicts (negative)": DatasetInfo(
            name="Gama Network of Alliances",
            filename="highlandtribes.csv",
            representation_type="Edge List",
            file_type="CSV",
            description="Collected by anthropologist Kenneth Read in 1954, it documents the political and social relationships among 16 sub-tribes of the Gahuku-Gama alliance system in the Eastern Highlands of New Guinea."
        )
    }

    @classmethod
    def get_available_names(cls) -> list[str]:
        """
         Retrieves a list of all registered dataset identifiers within the framework.

        Returns:
            list[str]: A list containing the specific lookup keys for all configured datasets.
        """
        return list(cls.DATASETS.keys())

    @classmethod
    def get_info(cls, name: str) -> DatasetInfo:
        """
        Fetches the metadata configuration block for a given dataset name.

        Args:
            name (str): The exact lookup key of the desired dataset.

        Returns:
            DatasetInfo: The structured metadata object containing file definitions and descriptions.

        Raises:
            KeyError: If the provided dataset name is not registered within the active dictionary.
        """
        return cls.DATASETS[name]

    @classmethod
    def get_file_path(cls, name: str) -> str:
        """
        Resolves the absolute native system path to the physical source file of a dataset.

        Utilizes the system-agnostic path compilation layout to join the central data directory 
        with the requested dataset filename.

        Args:
            name (str): The exact lookup key of the target dataset.

        Returns:
            str: The full path to the raw file asset on the current host system.
        """
        info = cls.get_info(name)
        return os.path.join(cls.DATA_DIR, info.filename)
