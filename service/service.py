from pathlib import Path
import pandas as pd
from analyzing.summarizer import Summarizer
from scraping.scraper import Scraper

scraper = Scraper()
summarizer = Summarizer()


def reviews_to_csv(
    url: str,
    count: int = 100,
    sort: str = "relevancy",
    destination: Path = "reviews.csv",
) -> pd.DataFrame:
    generator = scraper.extract_reviews(url, count, sort)
    reviews = pd.DataFrame(generator)
    reviews.columns = ["reviews"]
    reviews.to_csv(destination, index=False)
    return reviews


def summarize_reviews(source: Path) -> str:
    reviews = pd.read_csv(source)["reviews"].to_list()
    summary = summarizer.summarize(reviews)
    return summary


def aspect_based_sentiment_analysis():
    pass


def general_sentiment_analysis():
    pass
