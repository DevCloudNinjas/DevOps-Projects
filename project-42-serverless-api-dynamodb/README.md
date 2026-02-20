# terraform-serverless-rest-api-dynamodb
Lambda based REST API entirely through code - API Gateway, YAML &amp; Terraform
![5b454bae-5fd4-405d-a37d-6bafc3fcf889](https://github.com/joelwembo/terraform-aws-serverless-rest-api-dynamodb/assets/19718580/5b11c6c0-3931-4588-acf8-c268ca82f99a)

Serverless Applications with AWS Lambda and API Gateway

# Compilation

sam package --template-file template.yaml --output-template-file deploy.yaml --s3-bucket $SAM_CODE_BUCKET

- terraform init

- terraform plan

- terraform deploy

- terraform destroy

