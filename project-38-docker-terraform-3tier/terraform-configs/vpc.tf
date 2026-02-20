# Creating VPC
resource "aws_vpc" "taskvpc" {
  cidr_block       = "${var.vpc_cidr}"
  instance_tenancy = "default"tags = {
    Name = "Task VPC"
  }
}