variable "prefix" {
    description = "prefix prepended to names of all resources created"
    default = "aws-terraform-test"
}

variable "port" {
    description = "port the container exposes, that the load balancer should forward port 80 to"
    default = "4000"
}

variable "region" {
    description = "selects the aws region to apply these services to"
    default = "us-east-1"
}

variable "source_path" {
  description = "source path for project"
  default     = "./project"
}

variable "tag" {
  description = "tag to use for our new docker image"
  default     = "latest"
}

variable "envvars" {
  type=map(string)
  description = "variables to set in the environment of the container"
  default = {
  }
}
