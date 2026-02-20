terraform {
  backend "s3" {
    bucket         = "django-terraform-rds-1"
    region         = "us-east-1"
    key            = "state/terraform.tfstate"
    dynamodb_table = "mycomponents_tf_lockid"
    encrypt        = true
  }
}