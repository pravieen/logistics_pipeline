# crawlers/leadiq_crawler.py

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('leadiq_logger')

def crawl_leadiq_articles(output_dir='data/raw'):
    url = 'https://www.leadiq.com/blog'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to load LeadiQ blog page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select('a[class*="blog-card_link"]')[:5]

    article_data = []

    for article in articles:
        try:
            article_url = article['href']
            if not article_url.startswith("http"):
                article_url = "https://www.leadiq.com" + article_url

            article_page = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')

            title_tag = article_soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

            date_tag = article_soup.find('time')
            published_date = date_tag.get_text(strip=True) if date_tag else "No Date Found"

            content_div = article_soup.find('div', class_='blog-post-body')
            content = content_div.get_text(separator='\n', strip=True) if content_div else "No Content Found"

            article_data.append({
                'title': title,
                'url': article_url,
                'published_date': published_date,
                'content': content,
                'scraped_at': datetime.utcnow().isoformat()
            })

        except Exception as e:
            logger.error(f"Error scraping article: {e}")

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, 'leadiq_articles.json')

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Saved {len(article_data)} LeadiQ articles.")
