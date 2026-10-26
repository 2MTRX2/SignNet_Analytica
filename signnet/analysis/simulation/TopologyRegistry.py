# TopologyRegistry.py
from typing import Any, Dict
import networkx as nx

class TopologyRegistry:
    _REGISTRY: Dict[str, Dict[str, Any]] = {
        "Random network G(N, M) (Erdős-Rényi)": {
            "func": nx.gnm_random_graph,
            "params": {
                "m": {
                    "type": "int", 
                    "label": "Total number of edges (M)", 
                    "min": 1, 
                    "max": lambda n, orig_m=None: int((n * (n - 1)) / 2) if n > 1 else 1, 
                    "value": lambda n, orig_m=None: orig_m if orig_m is not None else min(10, int((n * (n - 1)) / 2)) if n > 1 else 1,
                    "help": "Exactly M edges will be placed randomly among all possible node pairs."
                }
            }
        }, 
        "Random network G(N, p) (Erdős-Rényi)": {
            "func": nx.erdos_renyi_graph,
            "params": {
                "p": {
                    "type": "float", 
                    "label": "Edge probability (p)", 
                    "min": 0.0, 
                    "max": 1.0, 
                    "value": 0.1,
                    "help": "Probability that any given pair of nodes is connected by an edge."
                }
            }
        },       
        "Scale-Free (Barabási-Albert)": {
            "func": nx.barabasi_albert_graph,
            "params": {
                "m": {
                    "type": "int", 
                    "label": "Number of new edges per step (m)", 
                    "min": 1, 
                    "max": lambda n, orig_m=None: n - 1,
                    "value": lambda n, orig_m=None: min(2, n - 1) if n > 1 else 1,
                    "help": "Number of edges to attach from a new node to existing nodes."
                }
            }
        },
        "Small-World (Watts-Strogatz)": {
            "func": nx.watts_strogatz_graph,
            "params": {
                "k": {
                    "type": "int", 
                    "label": "Neighbours inside the ring (k)", 
                    "min": 2, 
                    "max": lambda n, orig_m=None: (n - 2) if (n % 2 == 0) else (n - 1), 
                    "value": lambda n, orig_m=None: min(4, (n - 2) if (n % 2 == 0) else (n - 1)) if n > 4 else 2,
                    "help": "Each node is initially connected to its k nearest neighbours in a ring topology."
                },
                "p": {
                    "type": "float", 
                    "label": "Rewiring probability (p)", 
                    "min": 0.0, 
                    "max": 1.0, 
                    "value": 0.05,
                    "help": "The probability of rewiring each edge randomly to introduce shortcuts."
                }
            }
        }
    }

    @classmethod
    def get_available_topologies(cls) -> list[str]:
        """Returns all registered names of the different network topologies."""
        return list(cls._REGISTRY.keys())

    @classmethod
    def get_topology_data(cls, name: str) -> Dict[str, Any]:
        """
        Returns the configuration metadata and generation function for a specific topology.

        Args:
            name (str): The name of the registered topology.

        Returns:
            Dict[str, Any]: Dictionary containing the keys 'func' and 'params'.

        Raises:
            ValueError: If the topology name is not registered.
        """
        if name not in cls._REGISTRY:
            raise ValueError(f"Topology name '{name}' is not registered.")
        return cls._REGISTRY[name]

