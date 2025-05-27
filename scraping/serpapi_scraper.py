from rich import print
from serpapi import Client
import os
from typing import Generator
from dotenv import load_dotenv
from scraping.scraper import Scraper
from utils.utils import extract_walmart_product_id


class SerpapiScraper(Scraper):
    """
    A class to scrape product reviews from Walmart using the SerpApi API.
    """

    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("SERPAPI_API_KEY")
        self._client = Client(api_key=self._api_key)

    def extract_reviews(
        self, url: str, count: int = 100, sort: str = "relevancy"
    ) -> Generator:
        """
        Implementation specific to Walmart products using the SerpApi API.
        See base class for full documentation.
        """

        product_id = extract_walmart_product_id(url)
        params = {
            "api_key": self._api_key,
            "engine": "walmart_product_reviews",
            "product_id": product_id,
            "sort": sort,
        }

        search = self._client.search(params)
        response = search.as_dict()
        reviews = response["reviews"]

        for review in reviews:
            yield review["text"]
            count -= 1
            if count == 0:
                return

        next_page = search.next_page()
        while next_page and count > 0:
            response = next_page.as_dict()
            reviews = response["reviews"]
            for review in reviews:
                yield review["text"]
                count -= 1
            next_page = next_page.next_page()
