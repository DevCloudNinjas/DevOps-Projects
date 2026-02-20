# EC2 Instance for Maven Build
resource "aws_instance" "maven_build" {
  ami                  = aws_ami_from_instance.maven_ami.id
  instance_type        = "t2.micro"                          # Adjust as needed
  key_name             = aws_key_pair.this.key_name
  iam_instance_profile = aws_iam_instance_profile.maven_profile.name

  vpc_security_group_ids = [aws_security_group.maven_sg.id]

  tags = {
    Name = "Maven Build Instance"
  }

  user_data = <<-EOF
                #!/bin/bash
                # Clone the GitHub repository
                git clone https://github.com/DevCloudNinjas/DevOps-Projects.git
                
                # Update pom.xml with Sonar and JFrog details
                sed -i 's|SONAR_URL|${var.sonar_url}|g' /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/pom.xml
                sed -i 's|JFROG_URL|${var.jfrog_url}|g' /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/pom.xml
                
                # Create settings.xml file
                cat <<EOT > /home/ec2-user/project/DevOps-Projects/DevOps-Project-01/Java-Login-App/settings.xml
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
                
                # Run Maven build
                cd /home/ec2-user/DevOps-Projects/DevOps-Project-01/Java-Login-App/
                mvn clean install -s settings.xml
                
                # Run Sonar analysis
                mvn sonar:sonar \
                  -Dsonar.projectKey=${var.sonar_project_key} \
                  -Dsonar.organization=${var.sonar_organization} \
                  -Dsonar.host.url=${var.sonar_url} \
                  -Dsonar.login=${var.sonar_token}
              EOF
}

# IAM Role for EC2 to access SSM Parameter Store
resource "aws_iam_role" "maven_role" {
  name = "maven_ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
  role       = aws_iam_role.maven_role.name
}

resource "aws_iam_instance_profile" "maven_profile" {
  name = "maven_instance_profile"
  role = aws_iam_role.maven_role.name
}
