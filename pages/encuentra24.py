import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import extra_streamlit_components as stx
from scraper.encuentra24 import run

load_dotenv()
cookie_manager = stx.CookieManager()


def main():

    st.subheader("Encuentra24, ofertas de empleo")

    categories = ["Todos", "Informática"]
    options = list(range(len(categories)))
    value = st.selectbox("Categoria", options, format_func=lambda x: categories[x])

    file = f"data/encuentra24_{value}.csv"

    if not os.path.exists(file):
        run(value)

    df = pd.read_csv(f"data/encuentra24_{value}.csv")
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

main()