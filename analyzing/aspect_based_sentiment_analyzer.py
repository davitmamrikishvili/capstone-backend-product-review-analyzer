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
    ) -> List[tuple[str, dict[str, float]]]:
        """
        Analyze the sentiment of a given prompt for specific aspects.
        Args:
            prompt (str): The text to analyze.
            aspects (List[str]): List of aspects to analyze in the text.
            *args: Additional arguments for the pipeline.
            **kwargs: Additional keyword arguments for the pipeline.
        Returns:
            List[tuple[str, dict[str, float]]]: A list of tuples where each tuple contains:
                - aspect (str): The aspect being analyzed.
                - sentiment (dict[str, float]): A dictionary with sentiment labels as keys and their scores as values.
        """
        result = []
        for aspect in aspects:
            if aspect.casefold() not in prompt.casefold():
                continue
            result.append(
                (aspect, *self._pipeline(prompt, text_pair=aspect, *args, **kwargs))
            )
        return result
