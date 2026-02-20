resource "aws_eks_cluster" "eks" {
  name     = "pc-eks"
  role_arn = aws_iam_role.master.arn


  vpc_config {
    subnet_ids = [aws_subnet.public-1.id, aws_subnet.public-2.id]
  }

  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.AmazonEKSServicePolicy,
    aws_iam_role_policy_attachment.AmazonEKSVPCResourceController,
    aws_iam_role_policy_attachment.AmazonEKSVPCResourceController,
    #aws_subnet.pub_sub1,
    #aws_subnet.pub_sub2,
  ]

}
