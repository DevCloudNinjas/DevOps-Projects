# ----------------------------------------------------------------------
# Terraform Deploy template S3 Object from SAM File
# ----------------------------------------------------------------------
resource "aws_s3_bucket_object" "sam_deploy_object" {
  bucket = var.sam_code_bucket
  key    = "sam-deploy-templates/${var.app_name}-deploy-${timestamp()}.yaml"
  source = "../sam/deploy.yaml"
  etag   = filemd5("../sam/deploy.yaml")
}

# ----------------------------------------------------------------------
# SAM Stack 
# ----------------------------------------------------------------------
resource "aws_cloudformation_stack" "products_api_sam_stack" {
  name         = "${var.app_name}-sam-stack"
  capabilities = ["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"]
  parameters = {
    AppName = var.app_name
  }

  template_url = "https://${var.sam_code_bucket}.s3-ap-southeast-1.amazonaws.com/${aws_s3_bucket_object.sam_deploy_object.id}"
}
