####### modules/vpc/variables.tf

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
}

variable "access_ip" {
  description = "CIDR block reserved for administrative access in examples."
  type        = string
}

variable "public_sn_count" {
  description = "Number of public subnets to create."
  type        = number
}

variable "public_cidrs" {
  description = "CIDR blocks for public subnets."
  type        = list(string)
}

variable "instance_tenancy" {
  description = "VPC instance tenancy."
  type        = string
}

variable "tags" {
  description = "Name tag value applied to VPC resources."
  type        = string
}

variable "map_public_ip_on_launch" {
  description = "Whether instances launched in public subnets receive public IPs."
  type        = bool
}

variable "rt_route_cidr_block" {
  description = "Default route CIDR block for the public route table."
  type        = string
}
