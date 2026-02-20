###### vpc/outputs.tf 
output "aws_public_subnet" {
  value = aws_subnet.public_project102_subnet.*.id
}

output "vpc_id" {
  value = aws_vpc.project102.id
}
