# resource "aws_lb" "tomcat_lb" {
#   name               = "tomcat-nlb"
#   internal           = true
#   load_balancer_type = "network"
#   subnets            = [aws_subnet.app_public_subnet.id]
# }
#
# resource "aws_lb_target_group" "tomcat_tg" {
#   name     = "tomcat-tg"
#   port     = 8080
#   protocol = "TCP"
#   vpc_id   = aws_vpc.app_vpc.id
# }
#
# resource "aws_lb_listener" "tomcat" {
#   load_balancer_arn = aws_lb.tomcat_lb.arn
#   port              = 8080
#   protocol          = "TCP"
#
#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.tomcat_tg.arn
#   }
# }
#
# resource "aws_launch_configuration" "tomcat_lc" {
#   name_prefix     = "tomcat-"
#   image_id        = aws_instance.tomcat_instance.id
#   instance_type   = "t2.micro"
#   security_groups = [aws_security_group.tomcat_sg.id]
#   key_name        = aws_key_pair.this.key_name
#
#   user_data = <<-EOF
#               #!/bin/bash
#               # Deploy .war artifact from JFrog
#               wget -O /opt/tomcat/webapps/myapp.war https://your-jfrog-url/path/to/your/artifact.war
#               systemctl restart tomcat
#               EOF
#
#   lifecycle {
#     create_before_destroy = true
#   }
# }
#
# # resource "aws_launch_configuration" "tomcat_lc" {
# #   name_prefix     = "tomcat-"
# #   image_id        = aws_ami_from_instance.tomcat_ami.id
# #   instance_type   = "t2.micro"
# #   security_groups = [aws_security_group.tomcat_sg.id]
# #   key_name        = aws_key_pair.this.key_name
# #
# #   user_data = <<-EOF
# #               #!/bin/bash
# #               set -e  # Exit immediately if a command exits with a non-zero status
# #
# #               # Log file for debugging
# #               exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
# #
# #               echo "Deploying .war artifact from JFrog"
# #               wget -O /opt/tomcat/webapps/myapp.war ${var.jfrog_artifact_url}
# #
# #               echo "Restarting Tomcat"
# #               systemctl restart tomcat
# #
# #               echo "Deployment complete"
# #               EOF
# #
# #   lifecycle {
# #     create_before_destroy = true
# #   }
# # }
#
# resource "aws_autoscaling_group" "tomcat_asg" {
#   name                = "tomcat-asg"
#   vpc_zone_identifier = [aws_subnet.app_public_subnet.id]
#   target_group_arns   = [aws_lb_target_group.tomcat_tg.arn]
#   health_check_type   = "ELB"
#
#   min_size         = 2
#   max_size         = 4
#   desired_capacity = 2
#
#   launch_configuration = aws_launch_configuration.tomcat_lc.name
#
#   tag {
#     key                 = "Name"
#     value               = "Tomcat-Instance"
#     propagate_at_launch = true
#   }
# }
#
# # resource "aws_security_group" "tomcat_sg" {
# #   name        = "tomcat-sg"
# #   description = "Security group for Tomcat instances"
# #   vpc_id      = aws_vpc.app_vpc.id
# #
# #   ingress {
# #     from_port       = 22
# #     to_port         = 22
# #     protocol        = "tcp"
# #     security_groups = [aws_security_group.bastion_sg.id]
# #   }
# #
# #   ingress {
# #     from_port       = 8080
# #     to_port         = 8080
# #     protocol        = "tcp"
# #     cidr_blocks     = aws_vpc.app_vpc.cidr_block
# #   }
# #
# #   egress {
# #     from_port   = 0
# #     to_port     = 0
# #     protocol    = "-1"
# #     cidr_blocks = ["0.0.0.0/0"]
# #   }
# # }