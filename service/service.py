import pandas as pd
from scraping.scraper import Scraper

scraper = Scraper()


def reviews_to_csv(
    url: str,
    count: int = 100,
    sort: str = "relevancy",
    destination: str = "reviews.csv",
) -> pd.DataFrame:
    generator = scraper.extract_reviews(url, count, sort)
    reviews = pd.DataFrame(generator)
    reviews.columns = ["reviews"]
    reviews.to_csv(destination, index=False)
    return reviews
