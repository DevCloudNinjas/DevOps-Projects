# ----------------------------------------------------------------------
# API Gateway Invoke URL
# ----------------------------------------------------------------------
output "api_invoke_url" {
  value = aws_api_gateway_deployment.products_rest_api_deployment.invoke_url
}

# ----------------------------------------------------------------------
# API key
# ----------------------------------------------------------------------
output "api_key" {
  value     = nonsensitive(aws_api_gateway_api_key.api_key.value)
}