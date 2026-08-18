# CentralityResultFormatter.py
import pandas as pd
from typing import List, Dict, Iterable, Any

class CentralityResultFormatter:
    """
    Encapsulates the creation and standardization of centrality data representations.

    Provides a centralized utility interface to transform raw native Python data structures 
    — such as records, dictionaries, or parallel sequences — into strictly ordered, 
    index-aligned pandas DataFrame components ready for multi-metric concatenation.
    """

    @staticmethod
    def from_records(records: List[Dict[str, Any]], index_column: str = "node") -> pd.DataFrame:
        """
        Converts a list of row dictionaries into a standardized DataFrame with a fixed index.
        
        Args:
            records (List[Dict[str, Any]]): The raw list of dictionaries containing the structural 
                node names and their corresponding analytical metrics.
            index_column (str, optional): The column name to be extracted and used as the 
                primary DataFrame index. Defaults to "node".

        Returns:
            pd.DataFrame: A structured DataFrame indexed by the specified column, encapsulating 
                the provided metrics.
        """
        df = pd.DataFrame(records)
        return df.set_index(index_column)

    @staticmethod
    def from_dict(scores: Dict[str, float], metric_name: str) -> pd.DataFrame:
        """
        Converts a node-to-score dictionary into a standardized DataFrame.
        
        Args:
            scores (Dict[str, float]): A dictionary mapping unique node labels (keys) to 
                their calculated float centrality scores (values).
            metric_name (str): The canonical name of the centrality metric to serve as the 
                column identifier.

        Returns:
            pd.DataFrame: A single-column DataFrame indexed by node labels, isolating the 
                calculated metric scores.
        """
        rows = [{"node": node, metric_name: score} for node, score in scores.items()]
        return pd.DataFrame(rows).set_index("node")

    @staticmethod
    def from_array(nodes: Iterable, scores: Iterable, metric_name: str) -> pd.DataFrame:
        """
        Converts aligned node and score sequences into a standardized DataFrame.
        
        Args:
            nodes (Iterable): An iterable sequence containing the unique node labels, 
                ideally adhering to the framework's canonical node ordering.
            scores (Iterable): An iterable sequence of numeric centrality scores aligned 
                one-to-one with the positions in the nodes sequence.
            metric_name (str): The canonical name of the centrality metric to serve as the 
                column identifier.

        Returns:
            pd.DataFrame: A standardized DataFrame indexed by node labels, preserving the 
                linear mapping of computed scores.        
        """
        # taking each node with the corresponding score and creating a list containing dictionaries
        rows = [{"node": node, metric_name: score} for node, score in zip(nodes, scores)]
        return pd.DataFrame(rows).set_index("node")
