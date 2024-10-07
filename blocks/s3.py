import os

from dotenv import load_dotenv
from prefect_aws import AwsCredentials, S3Bucket

load_dotenv()

block_name_aws = os.getenv("PREFECT_BLOCK_AWS_CREDENTIALS")
block_s3_bucket = os.getenv("PREFECT_BLOCK_S3_BUCKET")
s3_bucket_name = os.getenv("AWS_BUCKET_NAME")

aws_credentials_block = AwsCredentials.load(block_name_aws)

s3_bucket_block = S3Bucket(
    bucket_name=s3_bucket_name,
    aws_credentials=aws_credentials_block,
)

s3_bucket_block.save(block_s3_bucket, overwrite=True)
