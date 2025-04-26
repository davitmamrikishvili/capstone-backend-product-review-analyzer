from transformers import pipeline
from typing import List, Union


class Summarizer:

    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline(
            "summarization", model="facebook/bart-large-cnn", *args, **kwargs
        )

    def summarize(self, prompt: Union[str, List[str]], *args, **kwargs) -> str:
        if isinstance(prompt, list):
            prompt = "".join(prompt)
        return self._pipeline(prompt, min_length=100, *args, **kwargs)[0][
            "summary_text"
        ]
