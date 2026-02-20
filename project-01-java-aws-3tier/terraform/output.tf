# Output AMI IDs
output "global_ami_id" {
  value = aws_ami_from_instance.global_ami.id
}

output "nginx_ami_id" {
  value = aws_ami_from_instance.nginx_ami.id
}

output "tomcat_ami_id" {
  value = aws_ami_from_instance.tomcat_ami.id
}

output "maven_ami_id" {
  value = aws_ami_from_instance.maven_ami.id
}


# Outputs
output "db_endpoint" {
  value = aws_db_instance.mysql.endpoint
}

# output "tomcat_nlb_dns" {
#   value = aws_lb.tomcat.dns_name
# }

# output "nginx_nlb_dns" {
#   value = aws_lb.nginx.dns_name
# }