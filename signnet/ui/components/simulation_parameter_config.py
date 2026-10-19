# simulation_parameter_config.py
from typing import Any, Dict
import streamlit as st

from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry

def configure_topology_parameters(selected_topology: str, number_of_nodes: int = None, neg_ratio_val: float = None, number_of_edges: int = None) -> Dict[str, Any]: 
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
        max_value=1000,
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
        step=0.01
    )
    global_parameters["neg_ratio"] = neg_ratio

    # 2. Topologie-spezifische Parameter laden
    topology_data = TopologyRegistry.get_topology_data(selected_topology)
    topo_params = topology_data["params"]

    for param_name, config in topo_params.items():
        
        raw_min = config.get("min")
        raw_max = config.get("max")
        raw_val = config.get("value")
        
        # dynamic adaption if it is lambda function
        min_val = raw_min(n, number_of_edges) if callable(raw_min) else raw_min
        max_val = raw_max(n, number_of_edges) if callable(raw_max) else raw_max
        default_val = raw_val(n, number_of_edges) if callable(raw_val) else raw_val
        
        if max_val is not None:
            default_val = min(default_val, max_val)
        
        if config["type"] == "float":
            val = st.slider(
                label=config["label"],
                min_value=min_val if min_val is not None else 0.0,
                max_value=max_val if max_val is not None else 1.0,
                value=config["value"],
                help=config.get("help", "")
            )
            
        elif config["type"] == "int":
            safe_min = int(min_val) if min_val is not None else None
            safe_max = int(max_val) if max_val is not None else None
            raw_val = int(default_val) if default_val is not None else 10
            
            safe_val = raw_val
            if safe_min is not None:
                safe_val = max(safe_min, safe_val)
            if safe_max is not None:
                if safe_min is not None and safe_max < safe_min:
                    safe_max = safe_min
                safe_val = min(safe_max, safe_val)

            # DIE LÖSUNG: Ein dynamischer Key zwingt Streamlit, das Widget neu zu bauen.
            # Er setzt sich aus der Topologie, dem Parameternamen und den aktuellen Grenzen zusammen.
            widget_key = f"int_{selected_topology}_{param_name}_min_{safe_min}_max_{safe_max}"

            val = st.number_input(
                label=config["label"],
                min_value=safe_min,
                max_value=safe_max,
                value=safe_val,
                step=1,
                help=config.get("help", ""),
                key=widget_key 
            )

            
        kwargs_parameters[param_name] = val

    return global_parameters, kwargs_parameters
