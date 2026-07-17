# signnet/io/data_representation/NetworkData.py
from dataclasses import dataclass
import pandas as pd
from typing import Optional, Iterable

@dataclass(frozen=True)
class NetworkData:
    """Immutable Container delivering the normalized network data."""
    edges: pd.DataFrame
    nodes: Optional[Iterable] = None
