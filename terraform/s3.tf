resource "aws_s3_bucket" "prefect-bucket" {
  bucket = "flows-bucket-${var.name}-${var.stage}"
  tags = {
    Name        = "My bucket Casptone Project"
    Environment = "Dev"
  }
}
