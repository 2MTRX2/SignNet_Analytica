# StateKeyGenerator.py

from signnet.models.SignedNetwork import SignedNetwork

from typing import Any, Dict, List, Optional

class StateKeyGenerator:
    """
    Generates deterministic, unique session state keys based on app configurations.
    Prevents cache/state misalignment when parameters change.
    """
    def __init__(self, prefix: str = "params"):
        self.prefix: str = prefix
        self._components: List[str] = []

    def add_network(self, network: SignedNetwork) -> "StateKeyGenerator":
        """Adds network dimensions to the key."""
        if network.nodes is not None and network.edges is not None:
            self._components.append(f"net_nodes_{len(network.nodes)}_edges_{len(network.edges)}")
        return self

    def add_flat_param(self, key: str, value: Any) -> "StateKeyGenerator":
        """Adds a simple key-value pair to the hash."""
        self._components.append(f"{key}_{value}")
        return self

    def add_dict(self, parameters: Dict[str, Any], prefix: str = "") -> "StateKeyGenerator":
        """Alphabetically sorts and adds a dictionary of parameters."""
        if not parameters:
            return self
        
        for p_name, p_val in sorted(parameters.items()):
            p_prefix = f"{prefix}_" if prefix else ""
            self._components.append(f"{p_prefix}{p_name}:{p_val}")
        return self

    def add_measures_with_parameters(self, selected_names: List[str], runtime_parameters: Dict[str, Dict[str, Any]]) -> "StateKeyGenerator":
        """
        Specialised method for the centrality/metrics logic. 
        Sorts measures and their sub-parameters dynamically.
        """
        for name in sorted(selected_names):
            self._components.append(name)
            if name in runtime_parameters:
                # Add sub-parameters sorted by name
                for p_name, p_val in sorted(runtime_parameters[name].items()):
                    self._components.append(f"{p_name}:{p_val}")
        return self

    def generate(self) -> str:
        """Assembles the final unique state key string."""
        return f"{self.prefix}_{'_'.join(self._components)}"

