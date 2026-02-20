# ----------------------------------------------------------------------
# CloudFormation exports for Lambda Function ARNs
# ----------------------------------------------------------------------
data "aws_cloudformation_export" "api_lambda_arn_cfn_exports" {
  for_each   = toset(var.api_lambda_functions)
  depends_on = [aws_cloudformation_stack.products_api_sam_stack]
  name       = "${var.app_name}-${each.value}-arn"
}

# ----------------------------------------------------------------------
# API Gateway Trust Policy
# ----------------------------------------------------------------------
data "aws_iam_policy_document" "apigateway_trust_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# ----------------------------------------------------------------------
# API Gateway Lambda execution policy
# ----------------------------------------------------------------------
data "aws_iam_policy_document" "apigateway_lambda_policy" {
  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = values(data.aws_cloudformation_export.api_lambda_arn_cfn_exports)[*].value
  }
}