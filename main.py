from transformers import pipeline

extractor = pipeline(model="google-bert/bert-base-uncased", task="feature-extraction")
result = extractor("This is a simple test.")

print(result)
