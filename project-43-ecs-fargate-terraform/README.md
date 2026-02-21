# **Deploying a Scalable Web App Using AWS ECS, ECR, and Fargate with Terraform**

## **Overview**
This project demonstrates how to deploy a fully containerized web application using **AWS Elastic Container Service (ECS) with Fargate**, **Elastic Container Registry (ECR)**, **Virtual Private Cloud (VPC)**, and **Elastic Load Balancer (ELB)** using **Terraform** for Infrastructure as Code (IaC).

## **Project Architecture**
The application follows this architecture:
- **Dockerized Application**: A web application (Node.js/Python/Go) is packaged into a Docker container.
- **Amazon ECR**: Stores the container image for deployment.
- **Amazon ECS (Fargate)**: Runs the containerized application in a serverless environment.
- **VPC Configuration**: Ensures secure networking with private and public subnets.
- **Application Load Balancer (ALB)**: Distributes traffic to running ECS tasks.
- **ECS Tasks & Services**: Define how the container runs and scales dynamically.

## 🛡️ 2026 DevSecOps Enhancements (What You Will Learn)
This repository demonstrates a foundational ECS Fargate deployment via Terraform. In a 2026 DevSecOps context, we emphasize two critical networking and IAM upgrades:
1. **Private Networking (VPC Endpoints):** Pulling images from ECR or writing logs to CloudWatch across the public internet is a security vulnerability and incurs NAT Gateway charges. Modern architectures utilize AWS PrivateLink (VPC Endpoints) to ensure sensitive container traffic never leaves the internal AWS backbone.
2. **IAM Task vs. Execution Roles:** Strict differentiation between IAM roles is enforced. The *Task Execution Role* is scoped purely to allow the ECS agent to pull images and write logs, while the *Task Role* is granted exclusively to the application code itself for interacting with AWS services (e.g., S3 or DynamoDB), enforcing least privilege boundaries.

## **Prerequisites**
Ensure you have the following installed:
- AWS CLI
- Terraform
- Docker
- AWS Account with necessary IAM permissions

## **Setup Instructions**

### **Step 1: Clone the Repository and Initialize Terraform**
```bash
git clone <repo-url>
cd <repo-directory>
terraform init
```

### **Step 2: Build and Push Docker Image to ECR**
```bash
# Authenticate AWS CLI
aws configure

# Build Docker image
docker build -t my-web-app .
```

Terraform will handle the creation of the **ECR repository** and the image push. Ensure Terraform applies before running the next command.

```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com

# Tag and push to ECR
docker tag my-web-app:latest <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/my-web-app:latest
docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/my-web-app:latest
```

### **Step 3: Apply Terraform Configuration**
```bash
terraform apply -auto-approve
```
This will:
- Provision an **ECS Cluster** and **Fargate Task Definition**
- Deploy the **VPC, Security Groups, and Subnets**
- Configure an **Application Load Balancer (ALB)**
- Set up the **ECS Service with Auto Scaling**

### **Step 4: Access the Application**
- Retrieve the ALB DNS name:
  ```bash
  terraform output alb_dns_name
  ```
- Open the ALB URL in your browser to access the application.

## **Bonus Enhancements**
- Implement **CI/CD using Terraform Cloud or GitHub Actions** for automated deployments.
- Enable **CloudWatch Logs** for monitoring and debugging.
- Use **Secrets Manager** for managing sensitive environment variables.

## **Conclusion**
This setup provides a **highly scalable, cost-effective, and secure** containerized web application deployed on AWS using Terraform for Infrastructure as Code. The architecture is fully managed, ensuring ease of maintenance and auto-scaling capabilities.

Happy Deploying! 🚀

