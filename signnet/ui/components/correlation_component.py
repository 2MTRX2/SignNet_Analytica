# correlation_component.py
import pandas as pd
import streamlit as st

from signnet.analysis.correlations.CorrelationAnalysis import CorrelationAnalysis
from signnet.analysis.correlations.CorrelationRegistry import CorrelationRegistry

def highlight_p_values(df: pd.DataFrame, alpha_level: float) -> pd.DataFrame:
    """
    Generates a conditional styling matrix for a pandas DataFrame based on statistical significance thresholds.

    Maps numerical p-values to visual CSS aesthetics by evaluating each coordinate against
    the provided alpha level. It marks diagonal self-correlations with an italicized neutral style,
    highlights statistically significant values in bold green, and mutes non-significant
    results in gray to maximize scannability.

    Args:
        df (pd.DataFrame): The symmetric matrix containing the calculated p-values 
            from the correlation analysis.
        alpha_level (float): The significance threshold below which a correlation is 
            considered statistically meaningful.

    Returns:
        pd.DataFrame: A matrix of identical dimensions containing CSS string declarations 
            ready for injection into the pandas Styler engine.
    """
    style_df = pd.DataFrame(
        "color: gray;", index=df.index, columns=df.columns
    )
    for col in df.columns:
        for idx in df.index:
            if idx == col:
                style_df.loc[idx, col] = (
                    "color: darkgray; font-style: italic;"
                )
            elif df.loc[idx, col] < alpha_level:
                style_df.loc[idx, col] = "color: green; font-weight: bold;"
    return style_df


def render_correlation_analysis(centrality_df: pd.DataFrame):
    """
    Orchestrates and renders the interactive correlation analysis interface within the Streamlit application.

    Evaluates the input centrality matrix and extracts available analytical metrics from the 
    CorrelationRegistry. It handles user interaction for metric and alpha-level selection, 
    triggers the behavioral strategy pattern inside the CorrelationAnalysis engine, and 
    presents the results via a dual-tabbed UI layout displaying gradient-mapped coefficients 
    and conditionally styled p-values.

    Args:
        centrality_df (pd.DataFrame): The input dataframe containing the calculated centrality 
            measures across network nodes, where columns represent individual metrics.

    Returns:
        None: This function handles side effects by rendering reactive UI widgets, tables, 
            and validation warnings directly into the active Streamlit view.
    """
    st.subheader("Correlation Analysis")

    # at least two centrality measures must be selected to perform a correlation analysis
    if centrality_df.shape[1] < 2:
        st.warning(
            "Please select at least two centrality measures to perform a correlation analysis."
        )
        return

    # create two columns which contain the selection boxes for the correlation metrics and the significance levels
    ctrl_col1, ctrl_col2 = st.columns(2)

    with ctrl_col1:
        ui_choice = st.selectbox(
            "Select Correlation Metric:",
            CorrelationRegistry.get_available_names(),
            key="correlation_metric_widget",
        )

    with ctrl_col2:
        alpha = st.selectbox(
            "Select Significance Level (Alpha):",
            [0.05, 0.01, 0.001, 0.10],
            index=0,
            format_func=lambda x: f"α = {x} ({(1-x)*100:.1f}% Confidence)",
            key="pvalue_widget",
        )

    # translate the name of the strategy into a specific strategy class e.g. "Spearman Rank Correlation (Recommended)" -> SpearmanStrategy
    corr_strategy = CorrelationRegistry.get_measure_class(ui_choice)()
    # initialise the analysis class
    analyzer = CorrelationAnalysis(strategy=corr_strategy)

    try:
        # calculate the correlations and corresponding p-values
        df_corr, df_p_values = analyzer.analyze_correlations(centrality_df)

        # create two tabs (one for correlations and one for p-values)
        tab1, tab2 = st.tabs(
            ["Correlation Coefficients", "p-Values (Significance)"]
        )

        with tab1:
            st.caption(
                "Values closer to 1.0 or -1.0 indicate strong positive or negative correlations."
            )
            st.dataframe(
                df_corr.style.background_gradient(
                    cmap="coolwarm", vmin=-1.0, vmax=1.0
                ),
                use_container_width=True,
            )

        with tab2:
            st.caption(
                f"Values below {alpha} indicate that the correlation is statistically significant."
            )
            formatted_p = df_p_values.style.format("{:.4e}").apply(
                highlight_p_values, alpha_level=alpha, axis=None
            )
            st.dataframe(formatted_p, use_container_width=True)

    except Exception as ex:
        st.error(f"Failed to calculate metric correlations:\n\n{ex}")
