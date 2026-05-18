output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "web_public_ip" {
  value = try(aws_instance.web[0].public_ip, null)
}

