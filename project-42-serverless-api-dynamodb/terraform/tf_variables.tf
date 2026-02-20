# ----------------------------------------------------------------------
# Default AWS Region used to deploy resources
# ----------------------------------------------------------------------
variable "aws_region" {
  default = "ap-southeast-1"
}


# S3 bucket for converted SAM templates
variable "sam_code_bucket" {
  default = "cloudapp-ecommerce"
}


# ----------------------------------------------------------------------
# Application name used for naming resources
# ----------------------------------------------------------------------
variable "app_name" {
  default = "products-api"
}

# ----------------------------------------------------------------------
# Lambda functions, used to retrieve function ARN CFN exports
# ----------------------------------------------------------------------
variable "api_lambda_functions" {
  default = [
    "get-controller",
    "put-controller"
  ]
}

# ----------------------------------------------------------------------
# Lambda invoke URI prefix used in openAPI specification
# ----------------------------------------------------------------------
variable "lambda_invoke_uri_prefix" {
  default = "arn:aws:apigateway:ap-southeast-1:lambda:path/2015-03-31/functions"
}


