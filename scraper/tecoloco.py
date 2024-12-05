import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time

load_dotenv()

DOMAIN = os.getenv("TECOLOCO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")

data = []


def scrape_page(html):
    jobs = html.find_all(class_="module job-result")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

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
            data.append(
                {
                    "cargo": title.upper(),
                    "empresa": company,
                    "lugar": city,
                    "oferta": link,
                    "expira": expires,
                }
            )


def run(value):
    pages = [
        "/empleos",
        "/empleo-informatica-internet",
    ]

    page_url = DOMAIN + pages[value]

    scraper = Scraper()
    html = scraper.fetch_page(page_url)

    pagination = html.find(id="pagination")
    pages = pagination.find_all("li")
    pages = pages[1:-1]

    scrape_page(html)

    productlink = []

    if len(pages) > 1:
        for i in range(2, 4):
            page = page_url + f"?Page={i}"
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
    df.to_csv(f"data/tecoloco_{value}.csv", index=False)
