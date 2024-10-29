import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper
from src.utils import string_to_boolean

load_dotenv()

API_URL = os.getenv("COMPUTRABAJO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")
USE_SELENIUM = string_to_boolean(os.getenv("USE_SELENIUM"))

LOCATIONS = {
    1: "/empleos-de-informatica-y-telecom-en-matagalpa",
    2: "/empleos-de-informatica-y-telecom-en-managua",
    3: "/empleos-de-informatica-y-telecom-en-leon",
    4: "/empleos-de-informatica-y-telecom-en-esteli",
    5: "/empleos-de-informatica-y-telecom-en-jinotega",
    6: "/empleos-de-informatica-y-telecom-en-masaya",
    7: "/empleos-de-informatica-y-telecom-en-granada",
}


def getLocation(option):
    location = LOCATIONS[option]
    return API_URL + location


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

            link = f'<a href="{API_URL}/{link}" target="_blank" >Oferta</a>'
            data.append([title, company, link, published])

    return data


st.subheader("Computrabajo Empleos")
st.write("Lista de empleos por la categoria de Informática")

locationOption = st.selectbox(
    "Seleccione Departamento",
    options=list(LOCATIONS.keys()),
    format_func=getLocation,
)

jobUrl = getLocation(locationOption)

scraper = Scraper(use_selenium=USE_SELENIUM, use_header=True)
html = scraper.fetch_page(jobUrl, use_header=True)

data = []
row = getJobsScraper(html)
data.append(row)

with st.spinner("Cargando datos..."):
    for i in range(2, 6):
        page = jobUrl + f"?p={i}"

        html = scraper.fetch_page(page, use_header=True)

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
