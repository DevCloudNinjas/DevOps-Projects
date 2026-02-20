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

