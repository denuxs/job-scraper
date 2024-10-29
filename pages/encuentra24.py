import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper

load_dotenv()

API_URL = os.getenv("ENCUENTRA24_URL")
PAGE_URL = API_URL + "/nicaragua-es/empleos-ofertas-de-trabajos?q=f_category1.16"
COMPANY_SKIP = os.getenv("COMPANY_SKIP")
USE_SELENIUM = os.getenv("USE_SELENIUM")


def getJobsScraper(html):
    jobs = html.find_all(
        class_="d3-ad-tile d3-ads-grid__item d3-ad-tile--fullwidth d3-ad-tile--bordered"
    )

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

    data = []
    for job in jobs:
        title = job.find(class_="d3-ad-tile__title").get_text(strip=True)
        location = job.find(class_="d3-ad-tile__location").get_text(strip=True)
        link = job.find(class_="d3-ad-tile__title").get("href")

        page = API_URL + link
        link = f'<a href="{page}" target="_blank">Oferta</a>'

        # if company not in companySkip:
        #     data.append([title, company, city, link, expires])

        data.append([title, location, link])

    return data


st.subheader("Encuentra24 Empleos")
st.write("Lista de empleos por la categoria de Informática")

scraper = Scraper(use_selenium=USE_SELENIUM)
html = scraper.fetch_page(PAGE_URL)

pagination = html.find(class_="d3-pagination")
pages = pagination.find_all("a")
pages = pages[1:-1]

data = []
row = getJobsScraper(html)
data.append(row)

with st.spinner("Cargando datos..."):
    if len(pages) > 1:
        for i in range(2, 4):
            page = PAGE_URL.replace("?", f".{i}?")

            html = scraper.fetch_page(page)

            if html:
                row = getJobsScraper(html)
                data.append(row)

scraper.close()

print("\n")
dataFlatten = [item for row in data for item in row]

columns = [["Cargo", "Lugar", "Oferta"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")
