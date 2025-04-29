from crawlers.crawler_logisticsoflogistics import crawl_logistics_of_logistics_articles
from crawlers.gnosisfreight_crawler import crawl_gnosisfreight_articles
from crawlers.freightwaves_crawler import crawl_freightwaves_articles
from crawlers.leadiq_crawler import crawl_leadiq_articles
from newsapi.newsapi_fetcher import fetch_newsapi_articles
from utils.s3_uploader import upload_file_to_s3
import os

def upload_all_files():
    local_data_dir = 'data/raw'
    for filename in os.listdir(local_data_dir):
        if filename.endswith('.json'):
            local_file_path = os.path.join(local_data_dir, filename)
            s3_path = f'raw_data/{filename}'
            upload_file_to_s3(local_file_path, s3_path)




def main():
    crawl_logistics_of_logistics_articles()
    crawl_gnosisfreight_articles()
    crawl_freightwaves_articles()
    crawl_leadiq_articles()
    fetch_newsapi_articles() 
    upload_all_files()

if __name__ == "__main__":
    main()



