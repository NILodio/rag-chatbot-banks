from prefect_aws import AwsCredentials, S3Bucket

aws_credentials = AwsCredentials(
    aws_access_key_id="your-access-key-id",
    aws_secret_access_key="your-secret-access-key",
)

aws_credentials.save(name="my-aws-creds", overwrite=True)

s3_bucket = S3Bucket(bucket_name="my-bucket", aws_credentials=aws_credentials)

s3_bucket.save(name="my-s3-bucket", overwrite=True)
