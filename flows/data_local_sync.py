import os

from dotenv import load_dotenv
from prefect import flow, get_run_logger
from prefect_aws import S3Bucket

load_dotenv()

block_s3_bucket = os.getenv("PREFECT_BLOCK_S3_BUCKET")
s3_bucket = S3Bucket.load(block_s3_bucket)


@flow
def download_s3_folder(s3_path, local_path):
    logger = get_run_logger()
    logger.info(f"Downloading PDFs from {s3_path} to {local_path}")
    s3_bucket.download_folder_to_path(from_folder=s3_path, to_folder=local_path)
    logger.info(f"Downloaded PDFs to {local_path}")


if __name__ == "__main__":
    download_s3_folder(s3_path="data/raw", local_path="data/raw")
