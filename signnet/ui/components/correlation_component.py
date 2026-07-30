# correlation_component.py
import pandas as pd
import streamlit as st

def highlight_p_values(df: pd.DataFrame, alpha_level: float) -> pd.DataFrame:
    """Creates a style DataFrame to highlight significant p-values."""
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


def render_correlation_analysis(
    centrality_df: pd.DataFrame, correlation_registry, analysis_class
):
    """Renders the entire correlation analysis section with tabs and styling."""
    st.subheader("Correlation Analysis")

    if centrality_df.shape[1] < 2:
        st.warning(
            "Please select at least two centrality measures to perform a correlation analysis."
        )
        return

    ctrl_col1, ctrl_col2 = st.columns(2)

    with ctrl_col1:
        ui_choice = st.selectbox(
            "Select Correlation Metric:",
            correlation_registry.get_available_names(),
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

    corr_strategy = correlation_registry.get_measure_class(ui_choice)()
    analyzer = analysis_class(strategy=corr_strategy)

    try:
        df_corr, df_p_values = analyzer.analyze_correlations(centrality_df)

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
