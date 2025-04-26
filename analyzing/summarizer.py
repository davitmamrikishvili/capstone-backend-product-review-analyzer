from transformers import pipeline
from typing import List, Union


class Summarizer:

    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline(
            "summarization", model="sshleifer/distilbart-cnn-12-6", *args, **kwargs
        )

    def summarize(self, prompt: Union[str, List[str]], *args, **kwargs) -> str:
        if isinstance(prompt, list):
            prompt = "\n".join(prompt)
        return self._pipeline(prompt, *args, **kwargs)[0]["summary_text"]
