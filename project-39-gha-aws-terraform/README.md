# 👉 GitHub-actions + AWS + Terraform #
![Github-actions Logo](/images/github-actions.png)

#### 👉 Repository to demonstrate Infrastructur-As-Code using: ####

 ```
  Github Actions Pipelines
  AWS
  Terraform + Terraform Cloud
 ```
 
 ## 👉 Task Workflow ##
 ![Task Logo](/images/tfc-gh-actions-workflow.png)

## 🛡️ 2026 DevSecOps Enhancements (What You Will Learn)
This repository leverages Terraform Cloud within the CI/CD pipeline, fulfilling a critical DevSecOps requirement: **Secure Remote State Management**. 
By utilizing Terraform Cloud (or an S3 backend with DynamoDB locking and KMS encryption), we guarantee that sensitive infrastructure state files (which often contain plaintext secrets, database passwords, and private IPs) are never committed to version control or left exposed on a Jenkins/GitHub Actions runner.
 
 ## 👉 AWS Components Used ##
 ```
 Virtual Private Cloud (VPC)
 Public Subnets
 EC2 Instance
 Internet Gateways (IG)
 Security Groups (SG)
 Elastic Container Registry (ECR)
 Elastic Container Service (ECS) + Fargate
 Auto Scaling Group (ASG)
 ```
 ![ECS-ECR-AWS Logo](/images/aws-ecs-ecr-github-actions.png)
 
 ## 👉 Project Info
 ![Project-info Logo](/images/Task-details.png)
 
 ## 👉 License

Copyright © 2022, [Harshhaa Reddy](https://github.com/harshhaareddy).
Released under the [GNU Affero General Public License v3.0](LICENSE).
 
