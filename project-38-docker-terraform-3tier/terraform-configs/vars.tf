variable "aws_region" {
  description = "AWS region used by this three-tier demo."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the demo VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for public web subnet 1."
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet1_cidr" {
  description = "CIDR block for public web subnet 2."
  type        = string
  default     = "10.0.2.0/24"
}

variable "subnet2_cidr" {
  description = "CIDR block for private application subnet 1."
  type        = string
  default     = "10.0.3.0/24"
}

variable "subnet3_cidr" {
  description = "CIDR block for private application subnet 2."
  type        = string
  default     = "10.0.4.0/24"
}

variable "subnet4_cidr" {
  description = "CIDR block for private database subnet 1."
  type        = string
  default     = "10.0.5.0/24"
}

variable "subnet5_cidr" {
  description = "CIDR block for private database subnet 2."
  type        = string
  default     = "10.0.6.0/24"
}

variable "admin_cidr_blocks" {
  description = "CIDR blocks allowed to SSH to web instances."
  type        = list(string)
  default     = ["203.0.113.0/24"]
}

variable "web_ingress_cidr_blocks" {
  description = "CIDR blocks allowed to reach public HTTP/HTTPS endpoints."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
