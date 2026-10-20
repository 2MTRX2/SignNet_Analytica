# grayout_stale_df.py
import pandas as pd
import streamlit as st

def is_stale(current_hash:str, expected_hash: str, button:str) -> bool: 
    if current_hash != expected_hash:
        st.warning(f"You changed parameters above. Click '{button}' to update the data, or proceed with the current results below.")
        return True
    else: 
        return False


def grayout_df(session_state_df:pd.DataFrame, is_stale:bool) -> pd.DataFrame: 
    # If the result doesn't apply to the current parameters, the dataframe is in gray style
    if is_stale:
        styled_df = session_state_df.style.map(lambda _: "color: rgba(120, 120, 120, 0.5);")
    else:
        styled_df = session_state_df

    return styled_df
