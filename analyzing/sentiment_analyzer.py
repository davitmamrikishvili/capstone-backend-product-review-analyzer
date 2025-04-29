from transformers import pipeline
from typing import List


class SentimentAnalyzer:

    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            *args,
            **kwargs
        )

    def analyze_sentiment(self, prompt: str, *args, **kwargs) -> List[dict]:
        """
        Analyze the sentiment of a given prompt.

        Args:
            prompt (str): The text to analyze.
            *args: Additional arguments for the pipeline.
            **kwargs: Additional keyword arguments for the pipeline.

        Returns:
            List[dict]: A dictionary in a list containing the sentiment label and score.
        """
        return self._pipeline(prompt, *args, **kwargs)
