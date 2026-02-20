resource "aws_internet_gateway" "main" {
  # The VPC ID to create in.
  vpc_id = aws_vpc.main.id

  # A map of tags to assign to the resource
  tags = {
    "Name" = "main"
  }
}