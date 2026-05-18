# Creating External LoadBalancer
resource "aws_lb" "external-alb" {
  name               = "external-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.tasksg.id]
  subnets            = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
}
resource "aws_lb_target_group" "target-elb" {
  name     = "alb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.taskvpc.id
}
resource "aws_lb_target_group_attachment" "attachment_1" {
  target_group_arn = aws_lb_target_group.target-elb.arn
  target_id        = aws_instance.taskinstance[0].id
  port             = 80

  depends_on = [
    aws_instance.taskinstance,
  ]
}
resource "aws_lb_target_group_attachment" "attachment_2" {
  target_group_arn = aws_lb_target_group.target-elb.arn
  target_id        = aws_instance.taskinstance1[0].id
  port             = 80

  depends_on = [
    aws_instance.taskinstance1,
  ]
}
resource "aws_lb_listener" "external-elb" {
  load_balancer_arn = aws_lb.external-alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target-elb.arn
  }
}
