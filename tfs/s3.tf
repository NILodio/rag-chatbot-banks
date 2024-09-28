resource "aws_s3_bucket" "prefect-bucket" {
  bucket = var.bucket_name
  tags = {
    Name        = "My bucket Casptone Project"
    Environment = "Dev"
  }
}
