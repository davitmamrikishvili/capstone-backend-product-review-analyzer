from pathlib import Path
from typing import List
import pandas as pd
from analyzing.aspect_based_sentiment_analyzer import AspectBasedSentimentAnalyzer
from analyzing.sentiment_analyzer import SentimentAnalyzer
from analyzing.summarizer import Summarizer
from scraping.scraper import Scraper

scraper = Scraper()

summarizer = Summarizer()
sentiment_analyzer = SentimentAnalyzer()
aspect_based_sentiment_analyzer = AspectBasedSentimentAnalyzer()


def reviews_to_csv(
    url: str,
    count: int = 100,
    sort: str = "relevancy",
    destination: Path = "reviews.csv",
) -> pd.DataFrame:
    """
    Scrape reviews from a given URL and save them to a CSV file.

    Args:
        url (str): The product URL to scrape reviews from
        count (int): Number of reviews to scrape. Defaults to 100.
        sort (str): Sorting method for reviews. Defaults to "relevancy".
        destination (Path): Path where the CSV file will be saved. Defaults to "reviews.csv".

    Returns:
        pd.DataFrame: DataFrame containing the scraped reviews.

    Example:
        >>> reviews_df = reviews_to_csv(
        ...     "https://www.walmart.com/ip/5074872077",
        ...     count=50,
        ...     sort="helpful",
        ...     destination=Path("product_reviews.csv")
        ... )
    """
    generator = scraper.extract_reviews(url, count, sort)
    reviews = pd.DataFrame(generator)
    reviews.columns = ["review"]
    reviews.to_csv(destination, index=False)
    return reviews


def summarize_reviews(source: Path) -> str:
    """
    Summarize the reviews.

    Args:
        source (Path): Path to the CSV file containing reviews.

    Returns:
        str: Summary of the reviews.
    """
    reviews = pd.read_csv(source)["review"].to_list()
    summary = summarizer.summarize(reviews)
    return summary


def aspect_based_sentiment_analysis(
    source: Path, destination: Path, aspects: List[str]
) -> dict[str, List[tuple[str, str, float]]]:
    """
    Analyze sentiment of reviews for specific aspects.

    Args:
        source (Path): Path to the CSV file containing reviews.
        destination (Path): Path to save the updated CSV file with sentiment analysis results.
        aspects (List[str]): List of aspects to analyze in the reviews.

    Returns:
        dict[str, List[tuple[str, str, float]]]: A dictionary where:
            - key: aspect name
            - value: list of tuples, each containing:
                - review text (str)
                - sentiment label (str)
                - sentiment score (float)
    """

    def extract_aspects(review, aspects):
        series = []
        for result in aspect_based_sentiment_analyzer.analyze_sentiment(
            review, aspects
        ):
            if result is []:
                continue
            aspect, sentiment = result
            label, score = sentiment["label"], round(sentiment["score"], 5)
            series.append([aspect, label, score])
        if series == []:
            return pd.Series([None, None, None])
        return pd.Series(*series)

    reviews_df = pd.read_csv(source)
    reviews_df[["aspect", "label", "score"]] = reviews_df["review"].apply(
        extract_aspects, args=(aspects,)
    )
    reviews_df.sort_values(
        by=["aspect", "label", "score"], ascending=[True, True, False], inplace=True
    )

    result = (
        reviews_df.groupby("aspect")
        .apply(
            lambda x: pd.Series(
                {
                    "positive_count": (x["label"] == "Positive").sum(),
                    "neutral_count": (x["label"] == "Neutral").sum(),
                    "negative_count": (x["label"] == "Negative").sum(),
                    "most_positive_review": (
                        x.loc[x[x["label"] == "Positive"]["score"].idxmax(), "review"]
                        if not x[x["label"] == "Positive"].empty
                        else None
                    ),
                    "most_negative_review": (
                        x.loc[x[x["label"] == "Negative"]["score"].idxmax(), "review"]
                        if not x[x["label"] == "Negative"].empty
                        else None
                    ),
                }
            )
        )
        .astype({"positive_count": int, "neutral_count": int, "negative_count": int})
        .to_dict(orient="index")
    )

    reviews_df.to_csv(destination, index=False)
    return result


def general_sentiment_analysis(
    source: Path, destination: Path
) -> tuple[int, int, str, str]:
    """
    Analyze sentiment of reviews and save results back to CSV.

    Args:
        source (Path): Path to the CSV file containing reviews.
        destination (Path): Path to save the updated CSV file with sentiment analysis results.

    Returns:
        tuple[int, int, str, str]: A tuple containing:
            - Number of positive reviews
            - Number of negative reviews
            - Most positive review (highest positive sentiment score)
            - Most negative review (highest negative sentiment score)
    """
    reviews_df = pd.read_csv(source)

    results = reviews_df["review"].apply(sentiment_analyzer.analyze_sentiment)

    reviews_df["sentiment_label"] = results.apply(lambda x: x[0]["label"])
    reviews_df["sentiment_score"] = results.apply(lambda x: round(x[0]["score"], 5))

    positive_df = reviews_df[reviews_df["sentiment_label"] == "POSITIVE"]
    negative_df = reviews_df[reviews_df["sentiment_label"] == "NEGATIVE"]

    positive_count = len(positive_df)
    negative_count = len(negative_df)

    most_positive_review = (
        positive_df.loc[positive_df["sentiment_score"].idxmax(), "review"]
        if not positive_df.empty
        else ""
    )

    most_negative_review = (
        negative_df.loc[negative_df["sentiment_score"].idxmax(), "review"]
        if not negative_df.empty
        else ""
    )

    reviews_df.to_csv(destination, index=False)

    return positive_count, negative_count, most_positive_review, most_negative_review
