variable "admin_cidr_blocks" {
  description = "CIDR blocks allowed to SSH to the kubectl server and EKS node remote access."
  type        = list(string)
  default     = ["203.0.113.0/24"]

  validation {
    condition     = length(var.admin_cidr_blocks) > 0
    error_message = "Provide at least one admin CIDR block, for example [\"203.0.113.10/32\"]."
  }
}
