# Creating Internet Gateway 
resource "aws_internet_gateway" "taskgateway" {
  vpc_id = "${aws_vpc.taskvpc.id}"
}