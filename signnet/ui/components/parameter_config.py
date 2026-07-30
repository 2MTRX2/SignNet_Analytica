# parameter_config.py
import streamlit as st

from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry


def configure_parameters(selected_names: list[str]): 
    """Dynamically renders Streamlit input widgets for chosen centrality measures' parameters.

    Iterates through the parameters defined in each class for each 
    selected measure. Based on the parameter boundaries and types, it renders 
    either an interactive slider or a numeric input field. Configured values 
    are collected and structured into a nested parameters dictionary.

    Args:
        selected_names (list[str]): Names of the centrality measures currently 
            selected by the user in the UI.

    Returns:
        dict[str, dict[str, float | int]]: A nested dictionary mapping each measure 
            name to a sub-dictionary of its parameter names and their current 
            UI-configured values (e.g., {'Signed Degree Centrality': {'beta': 0.85}}).
    """
    st.subheader("Configure Parameters")

    runtime_paramters = {}
        
    for name in selected_names:
        # Returns an instantiated class of the selected measure
        measure_class = CentralityRegistry.get_measure_class(name)

        # If the measure has parameters, the following code is executed
        if measure_class.PARAMETERS:
            st.markdown(f"**{name} Options**")
            runtime_paramters[name] = {}

            # Each parameter gets its own widget with (un-)defined limits
            for param in measure_class.PARAMETERS:
                # Typing
                cast = float if param.type == "float" else int
                default_step = 0.01 if param.type == "float" else 1
                step_val = cast(param.step) if param.step else default_step

                # Casting for limits
                min_v = cast(param.min_value) if param.min_value is not None else None
                max_v = cast(param.max_value) if param.max_value is not None else None
                def_v = cast(param.default)

                # Widget-choice: slider only if both limits are defined
                if min_v is None or max_v is None:
                    val = st.number_input(
                        param.label, min_value=min_v, max_value=max_v, value=def_v, step=step_val, key=f"{name}_{param.name}"
                    )
                    
                    # Validation errors if limits are exceeded
                    if min_v is not None and val < min_v:
                        st.error(f"{param.label} must be greater than or equal to {min_v}.")
                    if max_v is not None and val > max_v:
                        st.error(f"{param.label} must be less than or equal to {max_v}.")
                else:
                    # Create a slider if both sides have a limit
                    val = st.slider(
                        param.label, min_value=min_v, max_value=max_v, value=def_v, step=step_val, key=f"{name}_{param.name}"
                    )

                runtime_paramters[name][param.name] = val

    return runtime_paramters