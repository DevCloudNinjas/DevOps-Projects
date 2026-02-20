resource "aws_nat_gateway" "gw1" {
  # The allocation ID of the Elastic IP address for the gateway
  allocation_id = aws_eip.nat1.id

  # The subnet ID of the subnet in which to place the gateway
  subnet_id = aws_subnet.public_1.id

  # A map of tags to assign to the resource
  tags = {
    "Name" = "NAT 1"
  }
}

resource "aws_nat_gateway" "gw2" {
  # The allocation ID of the Elastic IP address for the gateway
  allocation_id = aws_eip.nat2.id

  # The subnet ID of the subnet in which to place the gateway
  subnet_id = aws_subnet.public_2.id

  # A map of tags to assign to the resource
  tags = {
    "Name" = "NAT 2"
  }
}