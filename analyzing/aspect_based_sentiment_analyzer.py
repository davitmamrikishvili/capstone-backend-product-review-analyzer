from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import List

class AspectBasedSentimentAnalyzer:
    
    def __init__(self, *args, **kwargs):
        model_name = "yangheng/deberta-v3-base-absa-v1.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self._pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, *args, **kwargs)

    def analyze_sentiment(self, prompt: str, aspects: List[str], *args, **kwargs) -> List[dict]:
        result = []
        for aspect in aspects:
            result.append((aspect, *self._pipeline(prompt, text_pair=aspect, *args, **kwargs)))
        return result


# aspect_based_sentiment_analyzer = AspectBasedSentimentAnalyzer()
# result = aspect_based_sentiment_analyzer.analyze_sentiment('The camera quality of this phone is amazing, but the Battery kinda sucks.',
#                                                   ['camera', 'phone', 'battery',])
# print(result)
# [('camera', {'label': 'Positive', 'score': 0.9976174235343933}), ('phone', {'label': 'Positive', 'score': 0.7831689715385437}), ('battery', {'label': 'Negative', 'score': 0.9960673451423645})]
