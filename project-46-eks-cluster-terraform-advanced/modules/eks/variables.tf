#######modules/eks/variables.tf

variable "aws_public_subnet" {
  description = "Public subnet IDs used by the EKS control plane and managed node group."
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID where the EKS cluster and node security group are created."
  type        = string
}

variable "cluster_name" {
  description = "Name of the EKS cluster."
  type        = string
}

variable "endpoint_private_access" {
  description = "Whether the private EKS API endpoint is enabled."
  type        = bool
}

variable "endpoint_public_access" {
  description = "Whether the public EKS API endpoint is enabled."
  type        = bool
}

variable "public_access_cidrs" {
  description = "CIDR blocks allowed to reach the public EKS API endpoint."
  type        = list(string)
}

variable "node_group_name" {
  description = "Name for the managed node group."
  type        = string
}

variable "scaling_desired_size" {
  description = "Desired managed node group size."
  type        = number
}

variable "scaling_max_size" {
  description = "Maximum managed node group size."
  type        = number
}

variable "scaling_min_size" {
  description = "Minimum managed node group size."
  type        = number
}

variable "instance_types" {
  description = "EC2 instance types allowed for the managed node group."
  type        = list(string)
}

variable "key_pair" {
  description = "EC2 key pair name used for node remote access in this demo."
  type        = string
}

variable "admin_cidr_block" {
  description = "CIDR block allowed to reach demo node security group ingress."
  type        = string
}
