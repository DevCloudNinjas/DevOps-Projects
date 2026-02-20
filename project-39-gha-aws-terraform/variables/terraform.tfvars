#region
region = "us-east-1"

#vpc
vpc_cidr = "10.0.0.0/16"
vpc_name = "gh-actions-aws-terraform"

#igw
igw_name = "gh-actions-aws-terraform_igw"

#subnets
subnet_cidr = ["10.0.0.0/24" ,"10.0.1.0/24"  ]
azs = ["us-east-1a", "us-east-1b" ]

#route table
pub_rt_name = "public_rt"