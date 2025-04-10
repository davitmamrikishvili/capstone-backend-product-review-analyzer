from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from analyzing.analyzer import Analyzer


app = FastAPI()
analyzer = Analyzer()

reviews = []

class Review(BaseModel):
    content: str


@app.get("/")
def read_root():
    return {"Hello": "qwerty"}

@app.post("/analyze/")
def analyze_me(review: Review):
    sentiment = analyzer.analyze_sentiment(review)
    print(review)
    print(sentiment)
    return {"sentiment-score": sentiment}



# aspect extraction, absa, sentiment analysis
# distilbert/distilbert-base-uncased-finetuned-sst-2-english