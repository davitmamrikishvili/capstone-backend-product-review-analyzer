from typing import List
import pandas as pd
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl, Field
from pathlib import Path
from model.model import Order
from service.service import (
    reviews_to_csv,
    summarize_reviews,
)


app = FastAPI(
    title="Review Analysis API",
    description="API for scraping and analyzing product reviews",
    version="1.0.0",
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


@app.post("/summarize/")
async def summarize(
    reviews: ReviewList,
):
    """
    Summarize reviews.
    """
    temp_file = "temp.csv"
    pd.DataFrame(reviews.reviews, columns=["review"]).to_csv(temp_file, index=False)
    summary = summarize_reviews(temp_file)
    return {"status": "success", "summary": summary}
