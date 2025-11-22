import logging
from bs4 import BeautifulSoup
from typing import List, Dict
from base_scraper import BaseJobScraper


class JobScraper(BaseJobScraper):
    COMPANY_SKIP = ["BairesDev LLC", "BairesDev"]
    DOMAIN = "https://www.tecoloco.com.ni"
    BASE_URL = f"{DOMAIN}/empleo-informatica-internet"

    def parse_jobs(self, html_content: str) -> List[Dict[str, str]]:
        """Parses job listings from HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        jobs = soup.find_all(class_="module job-result")
        data = []

        for job in jobs:
            try:
                title_tag = job.find("h2")
                title = title_tag.get_text(strip=True)
                link_suffix = title_tag.a.get("href")
                link = (
                    f"<a href='{self.DOMAIN}{link_suffix}' target='_blank'>Oferta</a>"
                )

                detail = job.find(class_="job-overview")
                company = detail.find(class_="name").get_text(strip=True)
                expires = detail.find(class_="updated-time").get_text(strip=True)
                city = detail.find(class_="location").get_text(strip=True)

                if company not in self.COMPANY_SKIP:
                    data.append(
                        {
                            "cargo": title.upper(),
                            "empresa": company,
                            "lugar": city,
                            "oferta": link,
                            "expira": expires,
                        }
                    )
            except AttributeError as e:
                logging.warning(f"Error parsing a job entry: {e}")
                continue

        return data

    def get_pagination_urls(self, html_content: str) -> List[str]:
        """Extracts pagination URLs from the initial page."""
        soup = BeautifulSoup(html_content, "html.parser")
        pagination = soup.find(id="pagination")
        if not pagination:
            return []

        pages = pagination.find_all("li")
        # Assuming the structure allows us to just take a range for now as per user request
        # In a real scenario, we might parse the last page number.
        # The user had logic: pages = pages[1:-1] and then range(2, 4)

        # User logic: pages = pages[1:-1] and check if len > 1
        pages = pages[1:-1]

        urls = []
        if len(pages) > 1:
            # Logic to fetch pages 2 and 3 as requested
            for i in range(2, 4):
                urls.append(f"{self.BASE_URL}?Page={i}")

        return urls


if __name__ == "__main__":
    with JobScraper() as scraper:
        scraper.run()
