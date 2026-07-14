# CentralityMeasure.py
from abc import ABC, abstractmethod

from signnet.models.StaticSignedNetwork import StaticSignedNetwork

class CentralityMeasure(ABC):
    """Abstract base class defining the uniform interface for all centrality algorithms.

    This class enforces the structural contract of the framework's analysis pipeline. 
    By accepting exclusively a 'SignedNetwork' domain object as input, it decouples 
    the core architecture from specific third-party graph processing libraries 
    (such as NetworkX or igraph) used inside the concrete implementations.

    All new centrality measures developed within the chair must inherit from this 
    class and implement 'compute' method.
    """

    @abstractmethod
    def compute(self, network: StaticSignedNetwork):
        """Executes the centrality calculation for the given signed network.

        Args:
            network (SignedNetwork): The validated, canonical domain model 
                containing the network topology and properties.

        Returns:
            dict or pd.DataFrame: A mapping of node identifiers to their 
                calculated centrality metrics. The exact format depends on 
                the specific mathematical requirements of the concrete measure.
        """
        pass
