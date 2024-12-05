import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper

load_dotenv()

DOMAIN = os.getenv("COMPUTRABAJO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")

data = []


def scrape_page(html):
    articles = html.find_all("article")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

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

            data.append(
                {
                    "cargo": title.upper(),
                    "empresa": company,
                    "oferta": link,
                    "publicado": published,
                }
            )


def run(value):

    pages = [
        "/empleos-en-managua",
        "/empleos-en-matagalpa",
        "/empleos-en-jinotega",
        "/empleos-en-esteli",
        "/empleos-en-leon¨",
        "/empleos-en-granada",
        "/empleos-en-masaya",
    ]

    page_url = DOMAIN + pages[value]

    scraper = Scraper(use_header=True)
    html = scraper.fetch_page(page_url)

    scrape_page(html)

    for i in range(2, 6):
        page = page_url + f"?p={i}"

        html = scraper.fetch_page(page)

        if html:
            scrape_page(html)

    scraper.close()

    df = pd.DataFrame(data)
    df.to_csv(f"data/computrabajo_{value}.csv", index=False)
