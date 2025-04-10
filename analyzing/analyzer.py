from transformers import pipeline

class Analyzer():
    def __init__(self):
        self._pipeline = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    
    def analyze_sentiment(self, prompt: str):
        return self._pipeline(prompt)
    

# import spacy
# from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# # load spacy model
# nlp = spacy.load("en_core_web_sm")

# # load pre-trained DeBERTa model for ABSA
# model_name = "yangheng/deberta-v3-base-absa-v1.1"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
# classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)



# def extract_aspects(text):
#     doc = nlp(text)
#     aspects = []
#     for chunk in doc.noun_chunks:  # extract noun phrases
#         if any(token.dep_ in ("nsubj", "dobj") for token in chunk):  # focus on key aspects
#             aspects.append(chunk.text)  # store the full noun phrase
#     return aspects


# def analyze_aspect_sentiment(text, aspects):
#     sentiment_results = {}
#     for aspect in aspects:
#         sentiment = classifier(text, text_pair=aspect)[0]['label']  # classify sentiment
#         sentiment_results[aspect] = sentiment
#     return sentiment_results

# # example text
# text = "The camera quality of this phone is amazing, but the battery life is disappointing."

# # extract aspects
# aspects = extract_aspects(text)
# print("Extracted Aspects:", aspects)

# # get sentiment for each aspect
# aspect_sentiments = analyze_aspect_sentiment(text, aspects)
# print("Aspect Sentiment Analysis:", aspect_sentiments)
