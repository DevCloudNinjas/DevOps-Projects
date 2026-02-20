output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "instance_dns_name" {
  value = aws_lb.staging.dns_name
}
