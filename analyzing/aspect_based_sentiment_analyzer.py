from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import List


class AspectBasedSentimentAnalyzer:

    def __init__(self, *args, **kwargs):
        model_name = "yangheng/deberta-v3-base-absa-v1.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self._pipeline = pipeline(
            "text-classification", model=model, tokenizer=tokenizer, *args, **kwargs
        )

    def analyze_sentiment(
        self, prompt: str, aspects: List[str], *args, **kwargs
    ) -> List[dict]:
        result = []
        for aspect in aspects:
            if aspect.casefold() not in prompt.casefold():
                continue
            result.append(
                (aspect, *self._pipeline(prompt, text_pair=aspect, *args, **kwargs))
            )
        return result
