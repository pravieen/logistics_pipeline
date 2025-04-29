# newsapi/newsapi_fetcher.py

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger('newsapi_logger')
load_dotenv()

def fetch_newsapi_articles(output_dir='data/raw'):
    API_KEY = os.getenv('NEWSAPI_KEY')
    URL = 'https://newsapi.org/v2/everything'

    query = 'logistics OR freight OR supply chain'
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
        'apiKey': API_KEY
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error fetching NewsAPI articles: {e}")
        return

    news_data = response.json().get('articles', [])
    
    articles = []
    for item in news_data:
        articles.append({
            'title': item.get('title'),
            'url': item.get('url'),
            'published_date': item.get('publishedAt'),
            'content': item.get('content'),
            'source': item.get('source', {}).get('name'),
            'scraped_at': datetime.utcnow().isoformat()
        })

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'newsapi_articles.json'), 'w') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Fetched {len(articles)} articles from NewsAPI")
