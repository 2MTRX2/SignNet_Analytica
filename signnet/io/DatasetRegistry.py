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
    """Registry that manages all predefined testing datasets in the framework."""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    DATASETS = {
        "Sampson Monks (Time 3)": DatasetInfo(
            name="Sampson Monks (Time 3)",
            filename="sampson_signed_t3.csv",
            representation_type="Adjacency Matrix",
            file_type="CSV",
            description="Sampsons famous network of 18 monks in a monastery. Consists of positive and negative relationships."
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
