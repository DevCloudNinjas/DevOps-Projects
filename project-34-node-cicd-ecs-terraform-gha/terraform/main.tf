# Provider Configuration
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.63.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# VPC Creation
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "my_subnet" {
  vpc_id = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24"
}

# Security Group Creation
resource "aws_security_group" "my_security_group" {
  name_prefix = "my-security-group"
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECR Repository Creation
resource "aws_ecr_repository" "my_repository" {
  name = "my-repository"
}

# ECS Cluster Creation
resource "aws_ecs_cluster" "my_cluster" {
  name = "my-cluster"
}

# ECS Task Definition Creation
resource "aws_ecs_task_definition" "my_task_definition" {
  family = "my-task-definition"
  container_definitions = jsonencode([
    {
      name = "my-container"
      image = "${aws_ecr_repository.my_repository.repository_url}:latest"
      network_mode            = "bridge"
      memory                  = 512
      memory_reservation      = 256
      portMappings = [
        {
          containerPort = 80
          hostPort = 80
        }
      ]
    }
  ])
}

# ECS Service Creation
resource "aws_ecs_service" "my_service" {
  name = "my-service"
  cluster = aws_ecs_cluster.my_cluster.id
  task_definition = aws_ecs_task_definition.my_task_definition.arn
  desired_count = 1
  launch_type = "EC2"
}

# Add Terraform Backend Service
terraform {
  backend "s3" {
    bucket = "terraformbackendaccess"
    key    = "terraformbackendaccess.tfstate"
    region = "us-east-1"
  }
}
