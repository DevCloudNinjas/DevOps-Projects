variable "environment" {
  description = "Deployment environment"
  type        = string
}

locals {
  cluster_name = "e2ecicd-eks-${var.environment}"

  
  vpc_cidrs = {
    dev     = "10.0.0.0/16"
    staging = "10.1.0.0/16"
    prod    = "10.2.0.0/16"
  }

  
  private_subnets = {
    dev     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
    staging = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
    prod    = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
  }

  public_subnets = {
    dev     = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
    staging = ["10.1.4.0/24", "10.1.5.0/24", "10.1.6.0/24"]
    prod    = ["10.2.4.0/24", "10.2.5.0/24", "10.2.6.0/24"]
  }
  
  instance_type = {
    dev     = "t3.small"
    staging = "t3.medium"
    prod    = "t3.large"
  }

  
  desired_instance_count = {
    dev     = 1
    staging = 2
    prod    = 3
  }
}

variable "ingress_nginx_namespace" {
  type        = string
  description = "The nginx ingress namespace (it will be created if needed)."
  default     = "ingress-nginx"
}

variable "region" {
  type    = string
  default = "ap-southeast-1"

}

