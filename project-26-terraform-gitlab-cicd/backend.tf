terraform {
  backend "s3" {
    bucket         = "s3statefile786"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "state-lock"
  }
}
