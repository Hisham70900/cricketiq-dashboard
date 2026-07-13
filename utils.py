import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    return pd.read_csv(
        "data/matches.csv",
        low_memory=False
    )


def format_number(number):
    return f"{int(number):,}"


def calculate_strike_rate(runs, balls):
    if balls == 0:
        return 0
    return round((runs / balls) * 100, 2)


def calculate_economy(runs, balls):
    if balls == 0:
        return 0
    return round((runs / balls) * 6, 2)