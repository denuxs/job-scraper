import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import extra_streamlit_components as stx
from scraper.tecoloco import run
import os

load_dotenv()
cookie_manager = stx.CookieManager()


def main():

    st.subheader("Tecoloco, ofertas de empleo")

    categories = ["Todos", "Informática"]
    options = list(range(len(categories)))
    value = st.selectbox("Categoria", options, format_func=lambda x: categories[x])

    file = f"data/tecoloco_{value}.csv"

    if not os.path.exists(file):
        run(value)

    df = pd.read_csv(f"data/tecoloco_{value}.csv")
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)


main()
