from typing import List
import pandas as pd
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl, Field
from pathlib import Path
from model.model import Order
from service.service import (
    aspect_based_sentiment_analysis,
    general_sentiment_analysis,
    reviews_to_csv,
    summarize_reviews,
)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Review Analysis API",
    description="API for scraping and analyzing product reviews",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Url(BaseModel):
    url: HttpUrl = Field(
        examples=["https://www.walmart.com/reviews/product/837853339"],
        description="The Walmart product URL to scrape reviews from",
    )


class ReviewList(BaseModel):
    reviews: List[str] = Field(
        examples=[
            [
                "Excellent build quality, very comfortable to use.",
                "Great battery life, lasts longer than expected!",
                "Buttons are sticky, difficult to press repeatedly.",
            ]
        ],
        description="List of reviews",
    )


@app.post("/scrape/")
async def scrape(
    url: Url,
    count: Annotated[
        int, Query(gt=0, le=1000, description="Number of reviews to scrape")
    ] = 100,
    sort: Annotated[
        Order, Query(description="Sorting method for the reviews")
    ] = Order.relevancy,
):
    """
    Scrape reviews from a product URL.
    """
    try:
        reviews = reviews_to_csv(
            str(url.url),
            count=count,
            sort=sort,
        )
        return {"status": "success", "reviews": reviews["review"].tolist()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analyze/")
async def analyze(
    reviews: ReviewList,
    aspects: Annotated[
        List[str],
        Query(
            description="List of aspects to analyze. Performs general sentiment analysis if not provided.",
            example=["battery", "buttons"],
        ),
    ] = None,
):
    """
    Analyze sentiment from a list of reviews.
    """
    try:
        temp_review_file = Path("temp.csv")
        temp_result_file = Path("temp_result.csv")
        pd.DataFrame(reviews.reviews, columns=["review"]).to_csv(
            temp_review_file, index=False
        )

        if aspects:
            aspect_based_sentiment_analysis(temp_review_file, temp_result_file, aspects)
            result_df = pd.read_csv(temp_result_file)

            grouped_df = result_df.groupby("review").apply(
                lambda group: group[["aspect", "label", "score"]].to_dict("records")
            )

            grouped_results = [
                {"review": review, "details": details}
                for review, details in grouped_df.items()
            ]

            return {
                "status": "success",
                "analysis_type": "aspect-based",
                "aspects_analyzed": aspects,
                "results": grouped_results,
            }

        else:
            general_sentiment_analysis(temp_review_file, temp_result_file)
            result_df = pd.read_csv(temp_result_file)

            grouped_df = result_df.groupby("review").apply(
                lambda group: group[["label", "score"]].to_dict("records")
            )

            grouped_results = [
                {
                    "review": review,
                    "label": details[0]["label"],
                    "score": details[0]["score"],
                }
                for review, details in grouped_df.items()
            ]

            return {
                "status": "success",
                "analysis_type": "general",
                "results": grouped_results,
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/summarize/")
async def summarize(
    reviews: ReviewList,
):
    """
    Summarize reviews.
    """
    try:
        temp_file = "temp.csv"
        pd.DataFrame(reviews.reviews, columns=["review"]).to_csv(temp_file, index=False)
        summary = summarize_reviews(temp_file)
        return {"status": "success", "summary": summary}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
