####### modules/vpc/variables.tf

variable "vpc_cidr" {}
variable "access_ip" {}
variable "public_sn_count" {}
variable "public_cidrs" {
  type = list(any)
}
variable "instance_tenancy" {

}
variable "tags" {

}
variable "map_public_ip_on_launch" {

}
variable "rt_route_cidr_block" {

}
