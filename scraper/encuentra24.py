import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper

load_dotenv()

DOMAIN = os.getenv("ENCUENTRA24_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")

data = []


def scrape_page(html):
    jobs = html.find_all(
        class_="d3-ad-tile d3-ads-grid__item d3-ad-tile--fullwidth d3-ad-tile--bordered"
    )

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

    for job in jobs:
        title = job.find(class_="d3-ad-tile__title").get_text(strip=True)
        location = job.find(class_="d3-ad-tile__location").get_text(strip=True)
        link = job.find(class_="d3-ad-tile__title").get("href")

        page = DOMAIN + link
        link = f'<a href="{page}" target="_blank">Oferta</a>'

        # if company not in companySkip:
        #     data.append([title, company, city, link, expires])

        data.append(
            {
                "cargo": title.upper(),
                "lugar": location,
                "oferta": link,
            }
        )


def run(value):

    pages = [
        "/nicaragua-es/empleos-ofertas-de-trabajos?",
        "/nicaragua-es/empleos-ofertas-de-trabajos?q=f_category1.16",
    ]

    page_url = DOMAIN + pages[value]

    scraper = Scraper()
    html = scraper.fetch_page(page_url)

    pagination = html.find(class_="d3-pagination")
    pages = pagination.find_all("a")
    pages = pages[1:-1]

    scrape_page(html)

    if len(pages) > 1:
        for i in range(2, 4):
            page = page_url.replace("?", f".{i}?")

            html = scraper.fetch_page(page)

            if html:
                scrape_page(html)

    scraper.close()

    df = pd.DataFrame(data)
    df.to_csv(f"data/encuentra24_{value}.csv", index=False)
