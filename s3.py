import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

# Create bucket if it doesn't exist
try:
    s3_client.head_bucket(Bucket=BUCKET_NAME)
except Exception:
    s3_client.create_bucket(Bucket=BUCKET_NAME)


def upload_graph(image_bytes, filename):
    """
    This function will upload a PNG image to MinIO and return the public URL.
    """
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=image_bytes,
        ContentType="image/png",
    )
    return f"{MINIO_ENDPOINT}/{BUCKET_NAME}/{filename}"
