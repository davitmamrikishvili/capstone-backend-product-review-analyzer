from transformers import pipeline
from typing import List, Union


class Summarizer:

    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline(
            "summarization", model="facebook/bart-large-cnn", *args, **kwargs
        )

    def summarize(self, prompt: Union[str, List[str]], *args, **kwargs) -> str:
        """
        Summarize the given text using a summarization pipeline.

        Args:
            prompt (Union[str, List[str]]): The text to summarize. Can be a single string or a list of strings.
            *args: Additional arguments for the pipeline.
            **kwargs: Additional keyword arguments for the pipeline.

        Returns:
            str: The summarized text.
        """
        if isinstance(prompt, list):
            prompt = "".join(prompt)
        return self._pipeline(prompt, min_length=100, *args, **kwargs)[0][
            "summary_text"
        ]
