import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import extra_streamlit_components as stx
from scraper.encuentra24 import run

load_dotenv()
cookie_manager = stx.CookieManager()

DOMAIN = os.getenv("ENCUENTRA24_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")


def main():

    st.subheader("Encuentra24, ofertas de empleo")

    categories = ["Todos", "Informática"]
    options = list(range(len(categories)))
    value = st.selectbox("Categoria", options, format_func=lambda x: categories[x])

    if cookie_manager.get("auth"):
        if st.button("Scrape data"):
            run(value)
            st.success("scrape ok")

    df = pd.read_csv(f"data/encuentra24_{value}.csv")
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

main()