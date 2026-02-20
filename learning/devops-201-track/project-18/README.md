# AUTOMATING INFRASTRUCTURE WITH IAC USING TERRAFORM PART 3 – REFACTORING

## INTRODUCTION

In continuation to Project 17, the entire code is refactored inorder to simplify the code using a Terraform tool called Module.

The following outlines detailed step taken to achieve this:


# STEP: Configuring A Backend On The S3 Bucket

By default the Terraform state is stored locally, to store it remotely on AWS using S3 bucket as the backend and also making use of DynamoDB as the State Locking the following setup is done:

- Creating a file called Backend.tf and entering the following code:

```
resource "aws_s3_bucket" "terraform-state" {
  bucket = "tony-terraform"
  force_destroy = true
}
resource "aws_s3_bucket_versioning" "version" {
  bucket = aws_s3_bucket.terraform-state.id
  versioning_configuration {
    status = "Enabled"
  }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "first" {
  bucket = aws_s3_bucket.terraform-state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

- Adding the following code which creates a DynamoDB table to handle locks and perform consistency checks:

```
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```
- Since Terraform expects that both S3 bucket and DynamoDB resources are already created before configuring the backend, executing terraform apply command:


![](./Images/terraform%20plan.PNG)

![](./Images/terraform%20plan1.PNG)

![](./Images/state%20list.PNG)



The implementation of terraform modularization for this project can be found in this repository:


[Terraform-modular-code-repo](https://github.com/Tonybesto/TCS-Modular-Terraform-Architecture)
