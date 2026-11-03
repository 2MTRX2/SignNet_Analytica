# simulation_parameter_config.py
from typing import Any, Dict, Union, cast
import streamlit as st

from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry
from signnet.utils.StateKeyGenerator import StateKeyGenerator


def configure_topology_parameters(
    selected_topology: str,
    number_of_nodes: int | None = None,
    neg_ratio_val: float | None = None,
    number_of_edges: int | None = None,
) -> tuple[Dict[str, Any], Dict[str, Any]]:
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
        number_of_edges (int, optional): Default value for the number of edges.

    Returns:
        tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing global parameters
            and topology-specific parameters.
    """
    st.markdown("#### Configure Topology Parameters")

    global_parameters: Dict[str, Any] = {}
    kwargs_parameters: Dict[str, Any] = {}

    n_iterations = st.number_input(
        label="Number of Iterations", min_value=1, max_value=1000, value=100, step=1
    )
    global_parameters["n_iterations"] = n_iterations

    n = st.number_input(
        label="Number of Nodes (n)", min_value=3, value=number_of_nodes or 100, step=1
    )
    global_parameters["n"] = n

    neg_ratio = st.number_input(
        label="Negative Ratio", min_value=0.0, max_value=1.0, value=neg_ratio_val or 0.1, step=0.01
    )
    global_parameters["neg_ratio"] = neg_ratio

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
            num_val = cast(Union[int, float], default_val)
            num_max = cast(Union[int, float], max_val)
            default_val = min(num_val, num_max)

        val: Any = None

        if config["type"] == "float":
            safe_min_input = cast(Any, min_val)
            safe_max_input = cast(Any, max_val)
            safe_def_input = cast(Any, default_val)

            safe_float_min: float = float(safe_min_input) if min_val is not None else 0.0
            safe_float_max: float = float(safe_max_input) if max_val is not None else 1.0
            safe_float_val: float = float(safe_def_input) if default_val is not None else 0.1

            val = st.slider(
                label=config["label"],
                min_value=safe_float_min,
                max_value=safe_float_max,
                value=safe_float_val,
                help=config.get("help", ""),
            )

        elif config["type"] == "int":
            safe_min_input = cast(Any, min_val)
            safe_max_input = cast(Any, max_val)
            safe_def_input = cast(Any, default_val)

            safe_min = int(safe_min_input) if min_val is not None else None
            safe_max = int(safe_max_input) if max_val is not None else None
            raw_val = int(safe_def_input) if default_val is not None else 10

            safe_val = raw_val
            if safe_min is not None:
                safe_val = max(safe_min, safe_val)
            if safe_max is not None:
                if safe_min is not None and safe_max < safe_min:
                    safe_max = safe_min
                safe_val = min(safe_max, safe_val)

            widget_key = (
                StateKeyGenerator(prefix="int")
                .add_flat_param("param", param_name)
                .add_flat_param("min", safe_min)
                .add_flat_param("max", safe_max)
                .generate()
            )

            val = st.number_input(
                label=config["label"],
                min_value=safe_min,
                max_value=safe_max,
                value=safe_val,
                step=1,
                help=config.get("help", ""),
                key=widget_key,
            )

        kwargs_parameters[param_name] = val

    return global_parameters, kwargs_parameters
