terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
    type = string
}

variable "vpc_id" {
    type = string
}

variable "key_name" {
    type = string
}

resource "aws_security_group" "jenkins_sg" {
  name        = "jenkins_sg"
  description = "Allow Jenkins Traffic"
  vpc_id      = var.vpc_id

  ingress {
    description      = "Allow from Personal CIDR block"
    from_port        = 8081
    to_port          = 8081
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "Allow SSH from Personal CIDR block"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "Jenkins SG"
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-2023.3.20240131.0-kernel-6.1-x86_64*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  owners = ["amazon"] # Canonical
}

resource "aws_iam_role" "test_role" {
  name = "test_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "test_profile" {
  name = "test_profile"
  role = "${aws_iam_role.test_role.name}"
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = "${aws_iam_role.test_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
     {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
     }
  ]
}
EOF
}

resource "aws_instance" "web" {
  ami             = data.aws_ami.amazon_linux.id
  instance_type   = "t2.xlarge" 
  key_name        = var.key_name
  iam_instance_profile = "${aws_iam_instance_profile.test_profile.name}"
  security_groups = [aws_security_group.jenkins_sg.name]
  user_data       = "${file("install_jenkins.sh")}"
  tags = {
    Name = "Jenkins"
  }
}

