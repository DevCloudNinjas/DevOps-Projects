resource "aws_vpc_peering_connection" "peer" {
  vpc_id      = aws_vpc.bastion_vpc.id # The VPC where your EC2 instances are
  peer_vpc_id = aws_vpc.app_vpc.id     # The VPC where your RDS instance is
  auto_accept = true

  tags = {
    Name = "VPC Peering between Bastion and App VPC"
  }
}

# Update route tables for both VPCs
resource "aws_route" "app_to_bastion" {
  route_table_id            = aws_route_table.app_private_rt.id
  destination_cidr_block    = aws_vpc.bastion_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}

resource "aws_route" "bastion_to_app" {
  route_table_id            = aws_route_table.bastion_public_rt.id
  destination_cidr_block    = aws_vpc.app_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}


