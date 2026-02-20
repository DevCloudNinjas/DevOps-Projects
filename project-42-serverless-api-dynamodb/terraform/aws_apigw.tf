# ----------------------------------------------------------------------
# API Gateway Execution Role
# ----------------------------------------------------------------------
resource "aws_iam_role" "apigateway_execution_role" {
  name               = "${var.app_name}-apigateway-role"
  path               = "/"
  description        = "Role assigned for API Gateway"
  assume_role_policy = data.aws_iam_policy_document.apigateway_trust_policy.json
}

# ----------------------------------------------------------------------
# API Gateway Lambda Invoke Permission Policy
# ----------------------------------------------------------------------
resource "aws_iam_policy" "lambda_permissions_policy" {
  name   = "${var.app_name}-lambda-permissions"
  path   = "/"
  policy = data.aws_iam_policy_document.apigateway_lambda_policy.json
}

# ----------------------------------------------------------------------
# API Gateway Lambda Invoke Permission Policy - Attachment
# ----------------------------------------------------------------------
resource "aws_iam_role_policy_attachment" "lambda_permissions_policy_attach" {
  role       = aws_iam_role.apigateway_execution_role.name
  policy_arn = aws_iam_policy.lambda_permissions_policy.arn
}

# ----------------------------------------------------------------------
# API Gateway
# ----------------------------------------------------------------------
resource "aws_api_gateway_rest_api" "products_rest_api" {
  depends_on = [aws_cloudformation_stack.products_api_sam_stack]
  name       = var.app_name
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  body = templatefile("./files/api-def-v1.yaml", {
    app_name                   = var.app_name,
    api_gateway_execution_role = aws_iam_role.apigateway_execution_role.arn
    get_data_uri               = "${var.lambda_invoke_uri_prefix}/${data.aws_cloudformation_export.api_lambda_arn_cfn_exports["get-controller"].value}/invocations"
    put_data_uri               = "${var.lambda_invoke_uri_prefix}/${data.aws_cloudformation_export.api_lambda_arn_cfn_exports["put-controller"].value}/invocations"
  })
}

# ----------------------------------------------------------------------
# API Gateway Deployment
# ----------------------------------------------------------------------
resource "aws_api_gateway_deployment" "products_rest_api_deployment" {
  depends_on  = [aws_api_gateway_rest_api.products_rest_api]
  rest_api_id = aws_api_gateway_rest_api.products_rest_api.id
  stage_name  = "v1"
  variables = {
    "deployed_at" = timestamp()
  }
}


resource "aws_api_gateway_api_key" "api_key" {
  name        = "${var.app_name}-key"
  description = "API Key for Products API"
}


resource "aws_api_gateway_usage_plan" "usage_plan" {
  name        = "${var.app_name}-usage-plan-${timestamp()}"
  description = "Usage plan for Products"
  api_stages {
    api_id = aws_api_gateway_rest_api.products_rest_api.id
    stage  = aws_api_gateway_deployment.products_rest_api_deployment.stage_name
  }
}

# ----------------------------------------------------------------------
# API Key - Usage Plan Mapping
# ----------------------------------------------------------------------
resource "aws_api_gateway_usage_plan_key" "usage_plan_key" {
  key_id        = aws_api_gateway_api_key.api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.usage_plan.id
}
