import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper

load_dotenv()

API_URL = os.getenv("TECOLOCO_URL")
PAGE_URL = API_URL + "/empleo-informatica-internet"
COMPANY_SKIP = os.getenv("COMPANY_SKIP")
USE_SELENIUM = os.getenv("USE_SELENIUM")


def getJobsScraper(html):
    jobs = html.find_all(class_="module job-result")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

    data = []
    for job in jobs:
        title = job.find("h2").get_text(strip=True)
        link = job.find("h2").a.get("href")

        page = API_URL + link
        link = f'<a href="{page}" target="_blank">Oferta</a>'

        detail = job.find(class_="job-overview")
        company = detail.find(class_="name").get_text(strip=True)
        expires = detail.find(class_="updated-time").get_text(strip=True)
        city = detail.find(class_="location").get_text(strip=True)

        if company not in companySkip:
            data.append([title, company, city, link, expires])

    return data


st.subheader("Tecoloco Empleos")
st.write("Lista de empleos por la categoria de Informática")

scraper = Scraper(use_selenium=USE_SELENIUM)
html = scraper.fetch_page(PAGE_URL)

pagination = html.find(id="pagination")
pages = pagination.find_all("li")
pages = pages[1:-1]

data = []
row = getJobsScraper(html)
data.append(row)

with st.spinner("Cargando datos..."):
    if len(pages) > 1:
        for i in range(2, 4):
            page = PAGE_URL + f"?Page={i}"

            html = scraper.fetch_page(page)

            if html:
                row = getJobsScraper(html)
                data.append(row)

scraper.close()

print("\n")
dataFlatten = [item for row in data for item in row]

columns = [["Cargo", "Empresa", "Lugar", "Oferta", "Expira"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")
