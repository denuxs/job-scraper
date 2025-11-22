import logging
from bs4 import BeautifulSoup
from typing import List, Dict
from base_scraper import BaseJobScraper


class JobScraper(BaseJobScraper):
    COMPANY_SKIP = ["BairesDev LLC", "BairesDev"]
    DOMAIN = "https://www.encuentra24.com"
    BASE_URL = f"{DOMAIN}/nicaragua-es/empleos-ofertas-de-trabajos?q=f_category1.16"

    def parse_jobs(self, html_content: str) -> List[Dict[str, str]]:
        """Parses job listings from HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        jobs = soup.find_all(
            class_="d3-ad-tile d3-ads-grid__item d3-ad-tile--fullwidth d3-ad-tile--bordered"
        )
        data = []

        for job in jobs:
            try:
                title_tag = job.find(class_="d3-ad-tile__title")
                title = title_tag.get_text(strip=True)

                location = job.find(class_="d3-ad-tile__location").get_text(strip=True)
                link = job.find(class_="d3-ad-tile__description").get("href")
                link = f'<a href="{self.DOMAIN}{link}" target="_blank">Oferta</a>'

                data.append(
                    {
                        "cargo": title.upper(),
                        "lugar": location,
                        "oferta": link,
                    }
                )
            except AttributeError as e:
                logging.warning(f"Error parsing a job entry: {e}")
                continue

        return data

    def get_pagination_urls(self, html_content: str) -> List[str]:
        """Extracts pagination URLs from the initial page."""
        soup = BeautifulSoup(html_content, "html.parser")
        pagination = soup.find(class_="d3-pagination")
        if not pagination:
            return []

        pages = pagination.find_all("a")
        # Assuming the structure allows us to just take a range for now as per user request
        # In a real scenario, we might parse the last page number.
        # The user had logic: pages = pages[1:-1] and then range(2, 4)

        # User logic: pages = pages[1:-1] and check if len > 1
        pages = pages[1:-1]

        urls = []
        if len(pages) > 1:
            # Logic to fetch pages 2 and 3 as requested
            for i in range(2, 4):
                urls.append(f"{self.BASE_URL.replace('?', f'.{i}?')}")

        return urls


if __name__ == "__main__":
    with JobScraper() as scraper:
        scraper.run()
