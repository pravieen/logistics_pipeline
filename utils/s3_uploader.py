import os
import boto3
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger('s3_uploader')

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_file_to_s3(local_file_path, s3_path):
    try:
        s3_client.upload_file(local_file_path, S3_BUCKET, s3_path)
        logger.info(f"✅ Uploaded: {local_file_path} ➜ s3://{S3_BUCKET}/{s3_path}")
    except Exception as e:
        logger.error(f"❌ Failed to upload {local_file_path}: {e}")
