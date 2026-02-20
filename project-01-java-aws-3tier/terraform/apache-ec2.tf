resource "aws_instance" "tomcat_instance" {
  ami           = aws_ami_from_instance.global_ami.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.this.key_name

  tags = {
    Name = "Tomcat Instance for Golden AMI"
  }

  user_data = <<-EOF
              #!/bin/bash
              # Update the system
              yum update -y

              # Install Java and Tomcat
              amazon-linux-extras install -y java-openjdk11
              amazon-linux-extras install -y tomcat8.5

              # Configure Tomcat
              sed -i 's/8080/80/' /etc/tomcat/server.xml

              # Start and enable Tomcat
              systemctl start tomcat
              systemctl enable tomcat

              # Create a sample web application
      cat <<EOT > /usr/share/tomcat/webapps/ROOT/index.jsp
      <%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
      <!DOCTYPE html>
      <html>
      <head>
          <title>Tomcat on EC2</title>
      </head>
      <body>
          <h1>Hello from Tomcat on EC2!</h1>
          <p>Server Info: <%= application.getServerInfo() %></p>
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
                    "tomcat": {
                      "measurement": [
                        {"name": "threads.busy", "unit": "Count"},
                        {"name": "threads.count", "unit": "Count"}
                      ],
                      "metrics_collection_interval": 60
                    }
                  }
                }
              }
              EOT

              # Restart CloudWatch agent to apply changes
              systemctl restart amazon-cloudwatch-agent
              EOF

  vpc_security_group_ids = [aws_security_group.tomcat_sg.id]

  associate_public_ip_address = true
}

resource "aws_security_group" "tomcat_sg" {
  name        = "tomcat-sg"
  description = "Security group for Tomcat instance"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP_ADDRESS/32"] # REPLACE THIS with your actual IP address
    description = "Allow SSH from administrator IP"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "Tomcat Security Group"
  }
}

resource "aws_ami_from_instance" "tomcat_ami" {
  name               = "tomcat-golden-ami"
  source_instance_id = aws_instance.tomcat_instance.id

  tags = {
    Name = "Apache Tomcat Golden AMI"
  }

  depends_on = [aws_instance.tomcat_instance]
}