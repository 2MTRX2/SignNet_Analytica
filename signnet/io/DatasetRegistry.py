# DatasetRegistry.py
import os
from dataclasses import dataclass

@dataclass
class DatasetInfo:
    name: str
    filename: str
    representation_type: str
    file_type: str
    description: str

class DatasetRegistry:
    """Registry that manages all predefined datasets in the framework."""

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
        return list(cls.DATASETS.keys())

    @classmethod
    def get_info(cls, name: str) -> DatasetInfo:
        return cls.DATASETS[name]

    @classmethod
    def get_file_path(cls, name: str) -> str:
        info = cls.get_info(name)
        return os.path.join(cls.DATA_DIR, info.filename)
