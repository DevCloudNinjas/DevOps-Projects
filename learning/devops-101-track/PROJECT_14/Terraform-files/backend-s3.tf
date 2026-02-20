terraform {
  backend "s3" {
    bucket = "vprofile-terraform-state-rd"  # replace with your s3 bucketname
    key    = "backend"
    region = "us-east-1"
  }
}
