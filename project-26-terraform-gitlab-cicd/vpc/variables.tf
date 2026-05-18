variable "admin_cidr_blocks" {
  description = "CIDR blocks allowed to SSH to the demo EC2 instance. Override with your workstation or VPN range."
  type        = list(string)
  default     = ["203.0.113.0/24"]
}
