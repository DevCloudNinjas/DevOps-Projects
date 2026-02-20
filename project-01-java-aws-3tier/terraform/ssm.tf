# SSM Parameter Store for sensitive data
resource "aws_ssm_parameter" "jfrog_username" {
  name  = "/maven/jfrog_username"
  type  = "SecureString"
  value = "your-jfrog-username"
}

resource "aws_ssm_parameter" "jfrog_password" {
  name  = "/maven/jfrog_password"
  type  = "SecureString"
  value = "your-jfrog-password"
}

resource "aws_ssm_parameter" "sonar_token" {
  name  = "/maven/sonar_token"
  type  = "SecureString"
  value = "your-sonar-token"
}

# Store the private key in SSM Parameter Store
resource "aws_ssm_parameter" "private_key" {
  name  = "/ec2/keypair/${aws_key_pair.this.key_name}"
  type  = "SecureString"
  value = tls_private_key.this.private_key_pem
}