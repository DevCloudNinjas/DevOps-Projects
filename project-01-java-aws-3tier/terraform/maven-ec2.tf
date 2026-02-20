resource "aws_instance" "maven_instance" {
  ami                         = aws_ami_from_instance.global_ami.id
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.this.key_name
  vpc_security_group_ids      = [aws_security_group.maven_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "Maven Instance for Golden AMI"
  }

  user_data = <<-EOF
              #!/bin/bash
              # Clone the GitHub repository
              git clone https://github.com/DevCloudNinjas/DevOps-Projects.git
              
              # Update pom.xml with Sonar and JFrog details
              sed -i 's|SONAR_URL|https://sonarcloud.io|g' ./DevOps-Projects/DevOps-Project-01/Java-Login-App/pom.xml
              sed -i 's|JFROG_URL|${var.jfrog_url}|g' ./DevOps-Projects/DevOps-Project-01/Java-Login-App/pom.xml
              
              # Create settings.xml file
              cat <<EOT > ./DevOps-Projects/DevOps-Project-01/Java-Login-App/settings.xml
              <settings>
                <servers>
                  <server>
                    <id>jfrog-repo</id>
                    <username>${var.jfrog_username}</username>
                    <password>${var.jfrog_password}</password>
                  </server>
                </servers>
              </settings>
              EOT
              
              # Update application.properties with MySQL connection string
              echo "spring.datasource.url=jdbc:mysql://${aws_db_instance.mysql.endpoint}/${var.mysql_database_name}" >> /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/src/main/resources/application.properties
              echo "spring.datasource.username=${aws_db_instance.mysql.username}" >> /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/src/main/resources/application.properties
              echo "spring.datasource.password=${aws_db_instance.mysql.password}" >> /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/src/main/resources/application.properties
              
              # Run Maven build
              cd /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/
              mvn clean install -s settings.xml
              
              # Run Sonar analysis
              mvn sonar:sonar \
                -Dsonar.projectKey=${var.sonar_project_key} \
                -Dsonar.organization=${var.sonar_organization} \
                -Dsonar.host.url=https://sonarcloud.io \
                -Dsonar.login=${var.sonar_token}
              EOF
}

resource "aws_security_group" "maven_sg" {
  name        = "maven-sg"
  description = "Security group for Maven instance"
  #vpc_id      = aws_vpc.bastion_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    #cidr_blocks = [aws_vpc.bastion_vpc.id.vpc_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Maven Security Group"
  }
}

resource "aws_ami_from_instance" "maven_ami" {
  name               = "maven-golden-ami"
  source_instance_id = aws_instance.maven_instance.id

  tags = {
    Name = "Apache Maven Golden AMI"
  }

  depends_on = [aws_instance.maven_instance]
}

