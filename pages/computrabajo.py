import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper
from src.utils import string_to_boolean

load_dotenv()

DOMAIN = os.getenv("COMPUTRABAJO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")

def getJobsScraper(html):
    articles = html.find_all("article")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

    data = []
    for article in articles:
        link = article.h2.a.get("href")
        title = article.h2.a.get_text(strip=True)

        paragraphes = article.find_all("p")
        company = paragraphes[0]

        if company.find("a"):
            company = company.a.get_text(strip=True)
        else:
            company = company.get_text(strip=True)

        if company not in companySkip:
            published = paragraphes[-2].get_text(strip=True)

            link = f'<a href="{DOMAIN}/{link}" target="_blank" >Oferta</a>'
            data.append([title.upper(), company, link, published])

    return data


st.subheader("Computrabajo, ofertas de empleo")

pages = [
    "/empleos-en-managua",
    "/empleos-en-matagalpa",
    "/empleos-en-jinotega",
    "/empleos-en-esteli",
    "/empleos-en-leon¨",
    "/empleos-en-granada",
    "/empleos-en-masaya",
]

categories = ["Managua", "Matagalpa", "Jinotega", "Esteli", "León", "Granada", "Masaya"]
options = list(range(len(categories)))
value = st.selectbox("Departamento", options, format_func=lambda x: categories[x])

page_url = DOMAIN + pages[value]

scraper = Scraper(use_header=True)
html = scraper.fetch_page(page_url)

data = []
row = getJobsScraper(html)
data.append(row)

with st.spinner("Cargando datos..."):
    for i in range(2, 6):
        page = page_url + f"?p={i}"

        html = scraper.fetch_page(page)

        if html:
            row = getJobsScraper(html)
            data.append(row)

scraper.close()

print("\n")
dataFlatten = [item for row in data for item in row]

columns = [["Cargo", "Empresa", "Oferta", "Publicado"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")
