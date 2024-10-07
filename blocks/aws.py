import os

from dotenv import load_dotenv
from prefect_aws import AwsCredentials

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
region_name = os.getenv("AWS_REGION")
block_name_aws = os.getenv("PREFECT_BLOCK_AWS_CREDENTIALS")


AwsCredentials(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=None,
    region_name=region_name,
).save(block_name_aws, overwrite=True)
