# signnet/utils/CentralityResultFormatter.py
import pandas as pd
from typing import List, Dict, Iterable, Any

class CentralityResultFormatter:
    """Encapsulates the creation and standardization of centrality data representations."""

    @staticmethod
    def from_records(records: List[Dict[str, Any]], index_column: str = "node") -> pd.DataFrame:
        """Converts a list of row dictionaries into a standardized DataFrame with a fixed index.

        Args:
            records (List[Dict[str, Any]]): The raw list of dictionaries containing row data.
            index_column (str): The column name to be used as the DataFrame index. Defaults to "node".

        Returns:
            pd.DataFrame: A structured DataFrame indexed by the specified column.
        """
        df = pd.DataFrame(records)
        return df.set_index(index_column)

    @staticmethod
    def from_dict(scores: Dict[str, float], metric_name: str) -> pd.DataFrame:
        """Converts a node-to-score dictionary into a standardized DataFrame."""
        rows = [{"node": node, metric_name: score} for node, score in scores.items()]
        return pd.DataFrame(rows).set_index("node")

    @staticmethod
    def from_array(nodes: Iterable, scores: Iterable, metric_name: str) -> pd.DataFrame:
        """Converts aligned node and score sequences into a standardized DataFrame."""
        rows = [{"node": node, metric_name: score} for node, score in zip(nodes, scores)]
        return pd.DataFrame(rows).set_index("node")
