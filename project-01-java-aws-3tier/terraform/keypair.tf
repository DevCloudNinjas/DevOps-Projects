# Generate the key pair
resource "tls_private_key" "this" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create the EC2 key pair
resource "aws_key_pair" "this" {
  key_name   = "my-keypair"
  public_key = tls_private_key.this.public_key_openssh
}

