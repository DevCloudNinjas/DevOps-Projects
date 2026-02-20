# Create Global AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "global_ami_instance" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.this.key_name

  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }

  tags = {
    Name = "Global AMI Instance"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y aws-cli
              yum install -y amazon-cloudwatch-agent
              yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
              systemctl enable amazon-ssm-agent
              systemctl start amazon-ssm-agent
              EOF
}

resource "aws_ami_from_instance" "global_ami" {
  name               = "global-ami"
  source_instance_id = aws_instance.global_ami_instance.id

  tags = {
    Name = "Global AMI"
  }

  depends_on = [aws_instance.global_ami_instance]
}