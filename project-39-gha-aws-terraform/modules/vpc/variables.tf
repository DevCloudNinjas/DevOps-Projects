#region
variable "region" {
    description = "The value of the region used"
}

#vpc
variable "vpc_cidr" {
    description = "The CIDR block of the vpc"
}

variable "vpc_name" {
    description = "The Name of the vpc"
}

#igw
variable "igw_name" {
    description = "The Name of the Internet Gateway"
}

#subnets
variable "subnet_cidr" {
    description = "The subnet CIDR block of the vpc"
}

variable "azs" {
    description = "The value of the Avalability zone"
}

#route table
variable "pub_rt_name" {
    description = "The Name of the Route table"
}

#instance
variable "imagename" {
   type = map
   default = {
     us-east-1 = "ami-083654bd07b5da81d"
     us-east-2 = "ami-0629230e074c580f2"
   }
}
