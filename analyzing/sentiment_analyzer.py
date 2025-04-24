from transformers import pipeline
from typing import List

class SentimentAnalyzer:
    
    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", *args, **kwargs)
    
    def analyze_sentiment(self, prompt: str, *args, **kwargs) -> List[dict]:
        return self._pipeline(prompt, *args, **kwargs)
    
# sentiment_analyzer = SentimentAnalyzer()
# result = sentiment_analyzer.analyze_sentiment("I love this product!")  # Example usage
# print(result) [{'label': 'POSITIVE', 'score': 0.9998855590820312}]
