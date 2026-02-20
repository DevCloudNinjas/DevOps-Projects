/*====
The VPC
======*/

resource "aws_vpc" "vpc" {
  cidr_block       = var.vpc_cidr
  instance_tenancy = "default"
  enable_dns_support = "true"

  tags = {
    Name = var.vpc_name

  }
}

/* Internet Gateway */

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = var.igw_name
  }
}

/* Routing table for public subnet */

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = var.pub_rt_name
  }
}



/* Public subnet */

resource "aws_subnet" "subnets" {
  count = length(var.subnet_cidr)
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = element(var.subnet_cidr, count.index)
  availability_zone = element(var.azs, count.index)


  tags = {
    Name = "public_subnet-${count.index+1}"


  }
}

/* Route table associations */

resource "aws_route_table_association" "public-rt-ass" {
  count = length(var.subnet_cidr)
  subnet_id      = element(aws_subnet.subnets.*.id, count.index)
  route_table_id = aws_route_table.public_rt.id
}

/*====
VPC's Default Security Group
======*/

resource "aws_security_group" "default" {
  name        = "gh-aws-terraform"
  description = "Default security group to allow inbound/outbound from the VPC"
  vpc_id      = "${aws_vpc.vpc.id}"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}