from abc import ABC, abstractmethod
from typing import Generator


class Scraper(ABC):
    """
    An abstract base class defining the interface for web scrapers.
    """

    @abstractmethod
    def extract_reviews(
        self, url: str, count: int = 100, sort: str = "relevancy"
    ) -> Generator:
        """
        Extract reviews from a given product URL.

        Args:
            url (str): The product URL to scrape reviews from.
            count (int): Number of reviews to extract. Default is 100.
            sort (str): Sorting method for the reviews. Default is "relevancy".

        Yields:
            str: The review content.
        """
        pass
