terraform {
  backend "s3" {
    bucket         = "tetris-bucket"
    region         = "us-east-1"
    key            = "Chatbot-UI/EKS-TF/terraform.tfstate"
    dynamodb_table = "Lock-Files"
    encrypt        = true
  }
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      version = ">= 4.0, < 6.0"
      source  = "hashicorp/aws"
    }
  }
}
