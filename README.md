# Review Sentiment Analysis Tool

A tool for scraping, analyzing, and summarizing product reviews. This project provides both a CLI and API interface for processing reviews from e-commerce platforms. Currently, supporting [Walmart](https://www.walmart.com).

## Features

- **Review Scraping**: Extract reviews from e-commerce platforms (using [ZenRows](https://app.zenrows.com))
- **Sentiment Analysis**: 
  - General sentiment analysis with positive/negative classification
  - Aspect-based sentiment analysis for specific product features
- **Review Summarization**: Generate concise summaries of multiple reviews
- **Multiple Interfaces**: 
  - Command Line Interface (CLI)
  - RESTful API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/review-sentiment-analysis.git
cd review-sentiment-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up API_KEY in .env (Optional, only needed if you want to scrape data)

## Usage

### CLI Interface

The tool provides three main commands:

1. **Scrape Reviews**
```bash
python main.py scrape https://www.walmart.com/ip/product-id --count 100 --order relevancy
```

2. **Analyze Reviews**
```bash
# General sentiment analysis
python main.py analyze reviews.csv result.csv

# Aspect-based sentiment analysis
python main.py analyze reviews.csv result.csv --aspect battery --aspect display
```

3. **Summarize Reviews**
```bash
python main.py summarize reviews.csv
```

### API Interface

Start the API server:
```bash
python main.py api
```

The API will be available at `http://127.0.0.1:8000`

## Project Structure

```
.
├── analyzing/               # Sentiment analysis and summarization modules
├── cli/                    # CLI interface components
├── api/                    # API interface components
├── scraping/              # Web scraping functionality
├── service/               # Core business logic
└── utils/                 # Utility functions
```

## Dependencies

- FastAPI - Web framework for API
- Transformers - NLP models for sentiment analysis
- Typer - CLI framework
- Rich - Terminal formatting
- Pandas - Data manipulation
- PyTorch - Deep learning framework

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Davit Mamrikishvili

## Acknowledgments

- [DeBERTa-v3](https://huggingface.co/yangheng/deberta-v3-base-absa-v1.1) for aspect-based sentiment analysis
- [DistilBERT](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) for general sentiment analysis
- [BART](https://huggingface.co/facebook/bart-large-cnn) for text summarization
