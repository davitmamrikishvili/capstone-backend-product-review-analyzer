from transformers import pipeline
from typing import List

class SentimentAnalyzer:
    
    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", *args, **kwargs)
    
    def analyze_sentiment(self, prompt: str, *args, **kwargs) -> List[dict]:
        return self._pipeline(prompt, *args, **kwargs)
    