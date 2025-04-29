import os
import requests
from typing import Generator
from dotenv import load_dotenv
from utils.utils import extract_walmart_product_id


class Scraper:
    """
    A class to scrape product reviews from Walmart using the ZenRows API.
    """

    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("API_KEY")
        self._base_url = "https://ecommerce.api.zenrows.com/v1/targets/walmart/reviews/"
        self._session = requests.Session()

    def extract_reviews(
        self, url: str, count: int = 100, sort: str = "relevancy"
    ) -> Generator:
        params = {
            "apikey": self._api_key,
            "sort": sort,
        }
        product_id = extract_walmart_product_id(url)
        response = self._session.get(
            f"{self._base_url}{product_id}", params=params
        ).json()
        review_count = min(count, response["review_count"])
        for review in response["product_reviews_list"]:
            yield review["review_content"]
            review_count -= 1
            if review_count == 0:
                return

        next_page = response["pagination"].get("next_page")
        while next_page and review_count > 0:
            params["url"] = next_page
            response = self._session.get(self._base_url, params=params).json()
            for review in response["product_reviews_list"]:
                yield review["review_content"]
                review_count -= 1
                if review_count == 0:
                    return
            next_page = response["pagination"].get("next_page")
