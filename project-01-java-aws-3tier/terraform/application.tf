# App VPC
resource "aws_vpc" "app_vpc" {
  cidr_block           = var.app_vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "App VPC"
  }
}

# Subnets for App VPC
resource "aws_subnet" "app_public_subnet" {
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "172.32.1.0/24"
  availability_zone = "us-east-1a" # Change this as needed

  tags = {
    Name = "App Public Subnet"
  }
}

resource "aws_subnet" "app_private_subnet" {
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "172.32.2.0/24"
  availability_zone = "us-east-1b" # Change this as needed

  tags = {
    Name = "App Private Subnet"
  }
}

resource "aws_internet_gateway" "app_igw" {
  vpc_id = aws_vpc.app_vpc.id

  tags = {
    Name = "App IGW"
  }
}

# NAT Gateway for App VPC
resource "aws_eip" "nat_eip" {
  #domain = "vpc"
}

resource "aws_nat_gateway" "app_nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.app_public_subnet.id

  tags = {
    Name = "App NAT Gateway"
  }
}

resource "aws_route_table" "app_public_rt" {
  vpc_id = aws_vpc.app_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.app_igw.id
  }

  tags = {
    Name = "App Public Route Table"
  }
}

resource "aws_route_table" "app_private_rt" {
  vpc_id = aws_vpc.app_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.app_nat_gateway.id
  }

  tags = {
    Name = "App Private Route Table"
  }
}



resource "aws_route_table_association" "app_public_rta" {
  subnet_id      = aws_subnet.app_public_subnet.id
  route_table_id = aws_route_table.app_public_rt.id
}

resource "aws_route_table_association" "app_private_rta" {
  subnet_id      = aws_subnet.app_private_subnet.id
  route_table_id = aws_route_table.app_private_rt.id
}

# Transit Gateway
resource "aws_ec2_transit_gateway" "tgw" {
  description = "Transit Gateway for VPC communication"
}

resource "aws_ec2_transit_gateway_vpc_attachment" "app_tgw_attachment" {
  subnet_ids         = [aws_subnet.app_public_subnet.id, aws_subnet.app_private_subnet.id]
  transit_gateway_id = aws_ec2_transit_gateway.tgw.id
  vpc_id             = aws_vpc.app_vpc.id
}

resource "aws_security_group_rule" "tomcat_to_rds" {
  type              = "egress"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  cidr_blocks       = [aws_vpc.app_vpc.cidr_block]
  security_group_id = aws_security_group.tomcat_sg.id
}