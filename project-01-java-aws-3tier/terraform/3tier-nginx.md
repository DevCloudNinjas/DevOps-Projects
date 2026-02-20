resource "aws_security_group" "nginx_sg1" {
  name        = "nginx-sg"
  description = "Security group for Nginx instances"
  vpc_id      = aws_vpc.app_vpc.id

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion_sg.id]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_autoscaling_group" "nginx" {
  name                = "nginx-asg"
  target_group_arns   = [aws_lb_target_group.nginx.arn]
  health_check_type   = "ELB"

  min_size         = 2
  max_size         = 4
  desired_capacity = 2

  launch_configuration = aws_launch_configuration.nginx.name

  tag {
    key                 = "Name"
    value               = "Nginx-Instance"
    propagate_at_launch = true
  }
}

# Nginx Frontend
resource "aws_lb" "nginx" {
  name               = "nginx-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = [aws_subnet.app_public_subnet.id, aws_subnet.bastion_public_subnet.id]
}

resource "aws_lb_target_group" "nginx" {
  name     = "nginx-tg"
  port     = 80
  protocol = "TCP"
  vpc_id   = module.app_vpc.vpc_id
}

resource "aws_lb_listener" "nginx" {
  load_balancer_arn = aws_lb.nginx.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.nginx.arn
  }
}

resource "aws_launch_configuration" "nginx" {
  name_prefix     = "nginx-"
  image_id        = aws_ami_from_instance.nginx_ami.id
  instance_type   = "t3.small"
  security_groups = [aws_security_group.nginx_sg1.id]
  key_name        = aws_key_pair.this.key_name

  user_data = <<-EOF
              #!/bin/bash
              # Update nginx.conf with proxy_pass rules
              sed -i 's/proxy_pass http:\/\/localhost/proxy_pass http:\/\/${aws_lb.tomcat.dns_name}:8080/g' /etc/nginx/nginx.conf
              systemctl reload nginx
              EOF

  lifecycle {
    create_before_destroy = true
  }
}