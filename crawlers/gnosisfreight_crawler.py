# crawlers/gnosisfreight_crawler.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
from utils.logger import get_logger

logger = get_logger(__name__)

def crawl_gnosisfreight_articles():
    url = "https://www.gnosisfreight.com/insights"
    response = requests.get(url)

    if response.status_code != 200:
        logger.error(f"Failed to fetch page: {url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    article_items = soup.find_all("div", {"role": "listitem"})

    for item in article_items:
        try:
            # Extract title
            title_tag = item.find("h3", class_="blog-card-title-2")
            title = title_tag.text.strip() if title_tag else "No Title"

            # Extract summary
            summary_tag = item.find("p", class_="blog-card-excerpt")
            summary = summary_tag.text.strip() if summary_tag else "No Summary"

            # Extract article URL
            link_tag = item.find("a", class_="card-3")
            article_url = link_tag['href'] if link_tag else "No URL"

            # Extract publish date
            date_tag = item.find("div", class_="badge-2")
            publish_date = date_tag.text.strip() if date_tag else "No Date"

            # Extract image URL
            img_tag = item.find("img", class_="blog-card-image-2")
            image_url = img_tag['src'] if img_tag else "No Image URL"

            articles.append({
                "title": title,
                "summary": summary,
                "url": article_url,
                "publish_date": publish_date,
                "image_url": image_url,
                "source": "gnosisfreight"
            })
        except Exception as e:
            logger.error(f"Error parsing article: {e}")

    # Save articles
    save_path = os.path.join("data", "raw", f"gnosisfreight_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w") as f:
        json.dump(articles, f, indent=4)

    logger.info(f"Saved {len(articles)} articles to {save_path}")
