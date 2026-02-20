# # Terminate the instance after AMI creation
# resource "null_resource" "terminate_global_instance" {
#   triggers = {
#     ami_id = aws_ami_from_instance.global_ami.id
#   }

#   provisioner "local-exec" {
#     command = <<-EOT
#       #!/bin/bash
#       set -e

#       # Check if AWS CLI is installed and configured
#       if ! command -v aws &> /dev/null; then
#         echo "AWS CLI is not installed. Please install it and configure with appropriate permissions."
#         exit 1
#       fi

#       # Terminate the instance
#       if aws ec2 terminate-instances --instance-ids ${aws_instance.global_ami_instance.id}; then
#         echo "Successfully terminated instance ${aws_instance.global_ami_instance.id}"
#       else
#         echo "Failed to terminate instance ${aws_instance.global_ami_instance.id}"
#         exit 1
#       fi
#     EOT
#   }

#   depends_on = [aws_ami_from_instance.global_ami]
# }

# resource "null_resource" "terminate_maven_instance" {
#   triggers = {
#     ami_id = aws_ami_from_instance.maven_ami.id
#   }

#   provisioner "local-exec" {
#     command = <<-EOT
#       #!/bin/bash
#       set -e

#       # Check if AWS CLI is installed and configured
#       if ! command -v aws &> /dev/null; then
#         echo "AWS CLI is not installed. Please install it and configure with appropriate permissions."
#         exit 1
#       fi

#       # Terminate the instance
#       if aws ec2 terminate-instances --instance-ids ${aws_instance.maven_instance.id}; then
#         echo "Successfully terminated instance ${aws_instance.maven_instance.id}"
#       else
#         echo "Failed to terminate instance ${aws_instance.maven_instance.id}"
#         exit 1
#       fi
#     EOT
#   }

#   depends_on = [aws_ami_from_instance.maven_ami]
# }

# resource "null_resource" "terminate_nginx_instance" {
#   triggers = {
#     ami_id = aws_ami_from_instance.nginx_ami.id
#   }

#   provisioner "local-exec" {
#     command = <<-EOT
#       #!/bin/bash
#       set -e

#       # Check if AWS CLI is installed and configured
#       if ! command -v aws &> /dev/null; then
#         echo "AWS CLI is not installed. Please install it and configure with appropriate permissions."
#         exit 1
#       fi

#       # Terminate the instance
#       if aws ec2 terminate-instances --instance-ids ${aws_instance.nginx_instance.id}; then
#         echo "Successfully terminated instance ${aws_instance.nginx_instance.id}"
#       else
#         echo "Failed to terminate instance ${aws_instance.nginx_instance.id}"
#         exit 1
#       fi
#     EOT
#   }

#   depends_on = [aws_ami_from_instance.nginx_ami]
# }