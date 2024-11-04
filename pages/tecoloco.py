import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper

load_dotenv()

DOMAIN = os.getenv("TECOLOCO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")

def scrape_page(html):
    jobs = html.find_all(class_="module job-result")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

    data = []
    for job in jobs:
        title = job.find("h2").get_text(strip=True)
        link = job.find("h2").a.get("href")

        page = DOMAIN + link
        link = f'<a href="{page}" target="_blank">Oferta</a>'

        detail = job.find(class_="job-overview")
        company = detail.find(class_="name").get_text(strip=True)
        expires = detail.find(class_="updated-time").get_text(strip=True)
        city = detail.find(class_="location").get_text(strip=True)

        if company not in companySkip:
            data.append([title.upper(), company, city, link, expires])

    return data


st.subheader("Tecoloco, ofertas de empleo")

pages = [
    "/empleos",
    "/empleo-informatica-internet",
]

categories = ["Todos", "Informática"]
options = list(range(len(categories)))
value = st.selectbox("Categoria", options, format_func=lambda x: categories[x])

page_url = DOMAIN + pages[value]

scraper = Scraper()
html = scraper.fetch_page(page_url)

pagination = html.find(id="pagination")
pages = pagination.find_all("li")
pages = pages[1:-1]

data = []
row = scrape_page(html)
data.append(row)

with st.spinner("Cargando datos..."):
    if len(pages) > 1:
        for i in range(2, 4):
            page = page_url + f"?Page={i}"

            html = scraper.fetch_page(page)

            if html:
                row = scrape_page(html)
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
