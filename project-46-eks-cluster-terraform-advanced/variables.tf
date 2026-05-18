variable "cluster_endpoint_public_access_cidrs" {
  description = "CIDR blocks allowed to reach the public EKS API endpoint. Override with an operator/admin IP range."
  type        = list(string)
  default     = ["203.0.113.0/24"]

  validation {
    condition     = length(var.cluster_endpoint_public_access_cidrs) > 0
    error_message = "Provide at least one API endpoint CIDR, for example [\"203.0.113.10/32\"]."
  }
}

variable "admin_cidr_block" {
  description = "CIDR block allowed for administrative access in demo security groups."
  type        = string
  default     = "203.0.113.0/24"
}
