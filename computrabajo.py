import logging
from bs4 import BeautifulSoup
from typing import List, Dict
from base_scraper import BaseJobScraper


class JobScraper(BaseJobScraper):
    COMPANY_SKIP = ["BairesDev LLC", "BairesDev"]
    DOMAIN = "https://ni.computrabajo.com"
    BASE_URL = f"{DOMAIN}/empleos-en-managua"
    HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    def parse_jobs(self, html_content: str) -> List[Dict[str, str]]:
        """Parses job listings from HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        jobs = soup.find_all("article")
        data = []

        for job in jobs:
            try:
                link = job.h2.a.get("href")
                title = job.h2.a.get_text(strip=True)

                paragraphes = job.find_all("p")
                company = paragraphes[0]

                if company.find("a"):
                    company = company.a.get_text(strip=True)
                else:
                    company = company.get_text(strip=True)

                if company not in self.COMPANY_SKIP:
                    published = paragraphes[-2].get_text(strip=True)
                    link = f'<a href="{self.DOMAIN}/{link}" target="_blank" >Oferta</a>'

                    data.append(
                        {
                            "cargo": title.upper(),
                            "empresa": company,
                            "oferta": link,
                            "publicado": published,
                        }
                    )
            except AttributeError as e:
                logging.warning(f"Error parsing a job entry: {e}")
                continue

        return data

    def get_pagination_urls(self, html_content: str) -> List[str]:
        """Extracts pagination URLs from the initial page."""
        urls = []
        # Logic to fetch pages 2 and 3 as requested
        for i in range(2, 6):
            urls.append(f"{self.BASE_URL}?p={i}")

        return urls


if __name__ == "__main__":
    with JobScraper() as scraper:
        scraper.run()
