# crawlers/logistics_of_logistics_crawler.py

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('crawler_logger')

def crawl_logistics_of_logistics_articles(output_dir='data/raw'):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    url = 'https://www.thelogisticsoflogistics.com/articles/'
    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch main page: {e}")
        return

    soup = BeautifulSoup(page.text, 'html.parser')
    article_tags = soup.find_all('h2', class_='entry-title')

    article_data = []

    for tag in article_tags[:5]:  # scrape only first 5 articles
        try:
            link_tag = tag.find('a')
            if not link_tag:
                continue

            article_url = link_tag['href']
            article_title = link_tag.get_text(strip=True)

            article_page = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')

            title_tag = article_soup.find('h1', class_='entry-title')
            title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

            date_tag = article_soup.find('span', class_='updated')
            if not date_tag:
                date_tag = article_soup.find('span', class_='published')
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
            logger.error(f"Failed to scrape article: {e}")

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, 'logistics_of_logistics_articles.json')

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Successfully scraped and saved {len(article_data)} articles!")

