# ----------------------------------------------------------------------
# AWS Provider
# ----------------------------------------------------------------------
provider "aws" {
  region = var.aws_region
}

# ----------------------------------------------------------------------
# Terraform S3 backend with DynamoDB Lock table
# ----------------------------------------------------------------------
terraform {
  backend "s3" {
    bucket         = "cloudapp-terraform-state"
    key            = "products-api.tfstate"
    dynamodb_table = "my-terraform-lock"
    region         = "ap-southeast-1"
    encrypt        = "true"
  }
}
