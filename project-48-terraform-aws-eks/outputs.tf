output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC id."

  # Setting an output value as sensitive prevents Terraform from showing the values in  in the messages from terraform plan and terraform apply.
  sensitive = false
}