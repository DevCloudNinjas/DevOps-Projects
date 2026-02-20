# Create Nginx Golden AMI
resource "aws_instance" "nginx_instance" {
  ami           = aws_ami_from_instance.global_ami.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.this.key_name
  # Ensure the instance has an associated public IP
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.nginx_sg.id]

  tags = {
    Name = "Nginx Instance for Golden AMI"
  }

  user_data = <<-EOF
              #!/bin/bash

              # Start and enable Nginx
              yum update -y
              amazon-linux-extras install nginx1 -y

              # Start and enable Nginx
              systemctl enable nginx
              systemctl start nginx

              # Create a custom index.html file
              cat <<EOT > /usr/share/nginx/html/index.html
              <!DOCTYPE html>
              <html>
              <head>
                  <title>Welcome to my EC2 Nginx Server</title>
              </head>
              <body>
                  <h1>Hello from EC2!</h1>
                  <p>This page is served by Nginx on an Amazon EC2 instance.</p>
              </body>
              </html>
              EOT

              # Configure CloudWatch custom metrics
              cat <<EOT > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
              {
                "metrics": {
                  "metrics_collected": {
                    "mem": {
                      "measurement": [
                        {"name": "mem_used_percent", "unit": "Percent"}
                      ],
                      "metrics_collection_interval": 60
                    },
                    "nginx": {
                      "metrics_collection_interval": 60,
                      "metrics_collected": {
                        "active_connections": {
                          "measurement": [
                            {"name": "active_connections", "unit": "Count"}
                          ]
                        }
                      }
                    }
                  }
                }
              }
              EOT

              # Restart CloudWatch agent to apply changes
              systemctl restart amazon-cloudwatch-agent

              # Restart Nginx to apply changes
              systemctl restart nginx
              EOF
}

# Create a security group for the Nginx instance
resource "aws_security_group" "nginx_sg" {
  name        = "nginx-sg"
  description = "Security group for Nginx instance"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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
    Name = "Nginx Security Group"
  }
}

resource "aws_ami_from_instance" "nginx_ami" {
  name               = "nginx-golden-ami"
  source_instance_id = aws_instance.nginx_instance.id

  tags = {
    Name = "Nginx Golden AMI"
  }

  depends_on = [aws_instance.nginx_instance]
}