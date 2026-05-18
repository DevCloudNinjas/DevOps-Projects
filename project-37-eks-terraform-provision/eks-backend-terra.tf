terraform {
  backend "s3" {
    bucket         = "BUCKET_NAME"
    key            = "backend/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dynamoDB_TABLE_NAME"
  }
}
