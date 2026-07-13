import os
import pandas as pd
import streamlit as st
import gdown

FILE_ID = "1prTsfh2QstiB-wxZIcn0Wtg9ULm8OCEc"
URL = f"https://drive.google.com/uc?id={FILE_ID}"

DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "matches.csv")


@st.cache_data
def load_data():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(DATA_PATH):
        gdown.download(URL, DATA_PATH, quiet=False)

    df = pd.read_csv(DATA_PATH)

    return df