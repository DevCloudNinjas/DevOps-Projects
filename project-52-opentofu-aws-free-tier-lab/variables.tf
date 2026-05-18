variable "aws_region" {
  description = "AWS region for the lab."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name used for resource tags."
  type        = string
  default     = "opentofu-free-tier-lab"
}

variable "create_instance" {
  description = "Set false if you only want networking resources."
  type        = bool
  default     = true
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH. Replace with your public IP slash 32 before creating an instance."
  type        = string
  default     = "0.0.0.0/0"
}

