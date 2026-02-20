resource "aws_iam_instance_profile" "instance-profile" {
  name = "Jenkins-instance-profile"
  role = aws_iam_role.iam-role.name
}