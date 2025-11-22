import logging
import requests
from typing import List, Dict, Optional
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import streamlit as st
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class BaseJobScraper(ABC):
    COMPANY_SKIP = ["BairesDev LLC", "BairesDev"]
    DOMAIN = ""
    BASE_URL = ""
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    def __init__(self):
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetches the HTML content of a page."""
        try:
            # Some sites might need specific headers, so we use self.HEADERS which can be overridden or updated in subclasses if needed,
            # but for now we'll use a default or what's on the instance.
            # Note: computrabajo had specific headers, others didn't explicitly set them in the fetch call but used default session.
            # We will use the headers defined in the class or instance.
            response = self.session.get(url, timeout=10, headers=self.HEADERS)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as errh:
            if response.status_code == 404:
                logging.error(f"Page not found: {url}")
            else:
                logging.error(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"Something went wrong: {err}")
        return None

    @abstractmethod
    def parse_jobs(self, html_content: str) -> List[Dict[str, str]]:
        """Parses job listings from HTML content."""
        pass

    @abstractmethod
    def get_pagination_urls(self, html_content: str) -> List[str]:
        """Extracts pagination URLs from the initial page."""
        pass

    def fetch_jobs_threaded(self, urls: List[str]) -> List[Dict[str, str]]:
        """Fetches jobs from multiple URLs concurrently."""
        job_data = []
        logging.info(f"Starting threaded fetch for {len(urls)} pages...")
        start_time = time.time()

        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(self.fetch_page, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    html = future.result()
                    if html:
                        jobs = self.parse_jobs(html)
                        job_data.extend(jobs)
                        logging.info(f"Fetched {len(jobs)} jobs from {url}")
                except Exception as exc:
                    logging.error(f"{url} generated an exception: {exc}")

        logging.info(
            f"Threaded fetch completed in {time.time() - start_time:.2f} seconds"
        )
        return job_data

    def run(self):
        """Main execution method."""
        logging.info(f"Fetching initial jobs from {self.BASE_URL}...")
        html_content = self.fetch_page(self.BASE_URL)

        if html_content:
            job_data = self.parse_jobs(html_content)
            logging.info(f"Fetched {len(job_data)} jobs from initial page.")

            pagination_urls = self.get_pagination_urls(html_content)
            if pagination_urls:
                additional_jobs = self.fetch_jobs_threaded(pagination_urls)
                job_data.extend(additional_jobs)

            df = pd.DataFrame(job_data)
            st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
        else:
            logging.error("Failed to retrieve content.")
