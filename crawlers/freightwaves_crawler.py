# crawlers/freightwaves_crawler.py

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('freightwaves_logger')

def crawl_freightwaves_articles(output_dir='data/raw'):
    url = 'https://www.freightwaves.com/news'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch FreightWaves main page: {e}")
        return

    soup = BeautifulSoup(page.text, 'html.parser')
    article_tags = soup.find_all('article', class_='post-preview')

    article_data = []

    for tag in article_tags[:5]:  # Only first 5 articles
        try:
            link_tag = tag.find('a')
            if not link_tag:
                continue
            article_url = link_tag['href']
            if not article_url.startswith("http"):
                article_url = "https://www.freightwaves.com" + article_url

            article_page = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')

            title_tag = article_soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

            date_tag = article_soup.find('time')
            published_date = date_tag.get_text(strip=True) if date_tag else "No Date Found"

            content_div = article_soup.find('div', class_='entry-content')
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
    filename = os.path.join(output_dir, 'freightwaves_articles.json')

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Saved {len(article_data)} FreightWaves articles.")
