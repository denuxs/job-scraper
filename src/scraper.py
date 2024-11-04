import requests
from bs4 import BeautifulSoup
import random
import time
from selenium.webdriver import Chrome, ChromeOptions, Remote
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import sys
from src.utils import string_to_boolean
import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = [
    "Mozilla/5.0 (Linux; Android 4.4.4; [HM NOTE|NOTE-III|NOTE2 1LTET) AppleWebKit/537.39 (KHTML, like Gecko)  Chrome/53.0.2111.335 Mobile Safari/536.6"
    "Mozilla / 5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.2; x64; en-US Trident / 4.0)"
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_8; like Mac OS X) AppleWebKit/536.13 (KHTML, like Gecko)  Chrome/50.0.2440.333 Mobile Safari/600.1"
    "Mozilla/5.0 (iPod; CPU iPod OS 11_1_7; like Mac OS X) AppleWebKit/603.49 (KHTML, like Gecko)  Chrome/51.0.1709.273 Mobile Safari/533.6"
]

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}


class Scraper:
    _sleepTime = [1, 2, 3, 4, 5]

    def __init__(self, use_header=False):
        self.use_selenium = string_to_boolean(os.getenv("USE_SELENIUM"))
        self.use_header = use_header
        self.driver = None

        if self.use_selenium:
            service = Service(ChromeDriverManager().install())
            options = ChromeOptions()
            options.add_argument("--headless=new")

            if self.use_header:
                options.add_argument("--user-agent=%s" % random.choice(USER_AGENT))
            # options.page_load_strategy = 'none'

            self.driver = Chrome(service=service, options=options)

            # options = ChromeOptions()
            # self.driver = Remote(command_executor="http://localhost:4444", options=options)
            self.driver.implicitly_wait(0.5)

    def fetch_page(self, url):
        try:
            if self.use_selenium:
                self.driver.get(url)
                page_source = self.driver.page_source
            else:
                if self.use_header:
                    response = requests.get(url, headers=HEADERS)
                else:
                    response = requests.get(url)
                print(response.status_code)

                if response.status_code == 404:
                    return None

                response.raise_for_status()
                page_source = response.content

                # avoid ban :v
                randomSleepTime = random.choice(self._sleepTime)
                print(f"Esperando {randomSleepTime} segundos")
                time.sleep(randomSleepTime)

            return BeautifulSoup(page_source, "html.parser")

        except Exception as e:
            print(f"Error al obtener contenido: {e}")
            return None

    def parse_with_beautifulsoup(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        return soup

    def close(self):
        if self.use_selenium and self.driver is not None:
            self.driver.quit()
