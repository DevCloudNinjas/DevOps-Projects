terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.52.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}