# Bastion VPC
resource "aws_vpc" "bastion_vpc" {
  cidr_block           = var.bastion_vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "Bastion VPC"
  }
}

# Subnets for Bastion VPC
resource "aws_subnet" "bastion_public_subnet" {
  vpc_id            = aws_vpc.bastion_vpc.id
  cidr_block        = "192.168.1.0/24"
  availability_zone = "us-east-1a" # Change this as needed

  tags = {
    Name = "Bastion Public Subnet"
  }
}

# Internet Gateways
resource "aws_internet_gateway" "bastion_igw" {
  vpc_id = aws_vpc.bastion_vpc.id

  tags = {
    Name = "Bastion IGW"
  }
}

# Route Tables
resource "aws_route_table" "bastion_public_rt" {
  vpc_id = aws_vpc.bastion_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.bastion_igw.id
  }

  tags = {
    Name = "Bastion Public Route Table"
  }
}

# Route Table Associations
resource "aws_route_table_association" "bastion_public_rta" {
  subnet_id      = aws_subnet.bastion_public_subnet.id
  route_table_id = aws_route_table.bastion_public_rt.id
}

resource "aws_ec2_transit_gateway_vpc_attachment" "bastion_tgw_attachment" {
  subnet_ids         = [aws_subnet.bastion_public_subnet.id]
  transit_gateway_id = aws_ec2_transit_gateway.tgw.id
  vpc_id             = aws_vpc.bastion_vpc.id
}

# Bastion Host
resource "aws_instance" "bastion" {
  ami           = data.aws_ami.amazon_linux_2.id # Amazon Linux 2 AMI, change as needed
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.bastion_public_subnet.id
  key_name      = aws_key_pair.this.key_name # Change this to your key pair

  vpc_security_group_ids = [aws_security_group.bastion_sg.id]

  tags = {
    Name = "Bastion Host"
  }
}

# Elastic IP for Bastion
resource "aws_eip" "bastion_eip" {
  #domain   = "vpc"
  instance = aws_instance.bastion.id
}

# Security Group for Bastion
resource "aws_security_group" "bastion_sg" {
  name        = "bastion-sg"
  description = "Security group for Bastion host"
  vpc_id      = aws_vpc.bastion_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Bastion Security Group"
  }
}

resource "aws_security_group_rule" "bastion_to_rds" {
  type              = "egress"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  cidr_blocks       = [aws_vpc.app_vpc.cidr_block]
  security_group_id = aws_security_group.bastion_sg.id
}