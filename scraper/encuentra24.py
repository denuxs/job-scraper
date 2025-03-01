import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time

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
        link = job.find(class_="d3-ad-tile__description").get("href")

        link = f'<a href="{DOMAIN}/{link}" target="_blank">Oferta</a>'

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

    productlink = []

    if len(pages) > 1:
        for i in range(2, 4):
            page = page_url.replace("?", f".{i}?")
            productlink.append(page)

    print("Running threaded:")
    threaded_start = time.time()
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for url in productlink:
            futures.append(executor.submit(scraper.fetch_page, url=url))
        for future in concurrent.futures.as_completed(futures):
            html = future.result()
            if html:
                scrape_page(html)

    print("Threaded time:", time.time() - threaded_start)

    scraper.close()

    df = pd.DataFrame(data)
    df.to_csv(f"data/encuentra24_{value}.csv", index=False)
