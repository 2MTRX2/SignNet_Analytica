# simulation_parameter_config.py
from typing import Any, Dict
import streamlit as st

from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry

def configure_topology_parameters(selected_topology: str, number_of_nodes: int = None, neg_ratio_val: float = None) -> Dict[str, Any]: 
    """Dynamically renders Streamlit input widgets for the chosen topology's parameters.

    Iterates through the parameters defined in the TopologyRegistry for the 
    selected network topology. Based on the parameter boundaries and types, it renders 
    either an interactive slider or a numeric input field. Configured values 
    are collected and structured into a flat parameters dictionary.

    Args:
        selected_topology (str): Name of the network topology currently 
            selected by the user in the UI.
        number_of_nodes (int, optional): Default value for the number of nodes.
        neg_ratio_val (float, optional): Default value for the negative edge ratio.

    Returns:
        Dict[str, Any]: A dictionary mapping parameter names to their current 
            UI-configured values (e.g., {'n': 100, 'neg_ratio': 0.3, 'p': 0.1}).
    """
    st.markdown("#### Configure Topology Parameters")

    global_parameters = {}
    kwargs_parameters = {}

    n_iterations = st.number_input(
        label="Number of Iterations",
        min_value=1,
        value= 100,
        step=1
    )
    global_parameters["n_iterations"] = n_iterations

    n = st.number_input(
        label="Number of Nodes (n)",
        min_value=3,
        value=number_of_nodes or 100,
        step=1
    )
    global_parameters["n"] = n

    neg_ratio = st.number_input(
        label="Negative Ratio",
        min_value=0.0,
        max_value=1.0,
        value=neg_ratio_val or 0.1,
        step=0.05
    )
    global_parameters["neg_ratio"] = neg_ratio

    # 2. Topologie-spezifische Parameter laden
    topology_data = TopologyRegistry.get_topology_data(selected_topology)
    topo_params = topology_data["params"]

    for param_name, config in topo_params.items():
        
        # Sicherstellen, dass optionale min/max Werte sicher ausgelesen werden
        min_val = config.get("min", None)
        max_val = config.get("max", None)
        
        if config["type"] == "float":
            val = st.slider(
                label=config["label"],
                min_value=min_val if min_val is not None else 0.0,
                max_value=max_val if max_val is not None else 1.0,
                value=config["value"],
                help=config.get("help", "")
            )
            
        elif config["type"] == "int":
            # INTELLIGENTER SCHUTZ: Wenn das Modell Barabási-Albert ist und der Parameter 'm' heisst,
            # darf m niemals grösser oder gleich n sein. Wir limitieren das UI hier live!
            if selected_topology == "Scale-Free (Barabási-Albert)" and param_name == "m":
                max_val = n - 1
            
            val = st.number_input(
                label=config["label"],
                min_value=min_val,
                max_value=max_val,
                value=min(config["value"], max_val) if max_val is not None else config["value"],
                step=1,
                help=config.get("help", "")
            )
            
        kwargs_parameters[param_name] = val

    return global_parameters, kwargs_parameters
