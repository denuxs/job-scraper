import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import extra_streamlit_components as stx
from scraper.computrabajo import run

load_dotenv()
cookie_manager = stx.CookieManager()


def main():
    st.subheader("Computrabajo, ofertas de empleo")

    categories = [
        "Managua",
        "Matagalpa",
        "Jinotega",
        "Esteli",
        "León",
        "Granada",
        "Masaya",
    ]
    options = list(range(len(categories)))
    value = st.selectbox("Departamento", options, format_func=lambda x: categories[x])

    file = f"data/computrabajo_{value}.csv"

    if not os.path.exists(file):
        run(value)

    df = pd.read_csv(f"data/computrabajo_{value}.csv")
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)


main()
