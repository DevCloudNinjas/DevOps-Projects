# terraform-serverless-rest-api-dynamodb
Lambda based REST API entirely through code - API Gateway, YAML &amp; Terraform
![5b454bae-5fd4-405d-a37d-6bafc3fcf889](https://github.com/joelwembo/terraform-aws-serverless-rest-api-dynamodb/assets/19718580/5b11c6c0-3931-4588-acf8-c268ca82f99a)

Serverless Applications with AWS Lambda and API Gateway

## 🛡️ 2026 DevSecOps Enhancements (What You Will Learn)
Serverless architectures offload OS-level patching to AWS, but they introduce new attack vectors. This project highlights 2026 serverless DevSecOps principles:
1. **API Gateway Exploitation Prevention:** A public-facing API Gateway must be fronted by **AWS WAF (Web Application Firewall)** to mitigate OWASP Top 10 API threats (like injection and parameter tampering) before they ever trigger Lambda invocations (preventing DoS billing attacks).
2. **Lambda IAM Least Privilege:** Each individual Lambda function must be scoped with a granular IAM execution role. A function writing to DynamoDB should *only* have `dynamodb:PutItem` on that specific table ARN, not `dynamodb:*` across the account.

# Compilation

sam package --template-file template.yaml --output-template-file deploy.yaml --s3-bucket $SAM_CODE_BUCKET

- terraform init

- terraform plan

- terraform deploy

- terraform destroy

