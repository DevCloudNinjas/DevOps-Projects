resource "aws_elastic_beanstalk_environment" "vprofile-bean-prod" {
  application         = aws_elastic_beanstalk_application.vprofile-prod.name
  name                = "vprofile-bean-prod"
  solution_stack_name = "64bit Amazon Linux 2 v4.1.1 running Tomcat 8.5 Corretto 11"
  cname_prefix        = "vprofile-bean-prod-rd"

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = module.vpc.vpc_id
  }

  setting {
    name      = "IamInstanceProfile"
    namespace = "aws:autoscaling:launchconfiguration"
    value     = "aws-elasticbeanstalk-ec2-role"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", [module.vpc.private_subnets[0], module.vpc.private_subnets[1], module.vpc.private_subnets[2]])
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "AssociatePublicIpAddress"
    value     = "false"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = join(",", [module.vpc.public_subnets[0], module.vpc.public_subnets[1], module.vpc.public_subnets[2]])
  }

  setting {
    name      = "InstanceType"
    namespace = "aws:autoscaling:launchconfiguration"
    value     = "t2.micro"
  }

  setting {
    name      = "EC2KeyName"
    namespace = "aws:autoscaling:launchconfiguration"
    value     = aws_key_pair.vprofilekey.key_name
  }
  setting {
    name      = "Availability Zones"
    namespace = "aws:autoscaling:asg"
    value     = "Any 3"
  }

  setting {
    name      = "MinSize"
    namespace = "aws:autoscaling:asg"
    value     = "1"
  }

  setting {
    name      = "MaxSize"
    namespace = "aws:autoscaling:asg"
    value     = "4"
  }

  setting {
    name      = "environment"
    namespace = "aws:elasticbeanstalk:application:environment"
    value     = "prod"
  }

  setting {
    name      = "SystemType"
    namespace = "aws:elasticbeanstalk:healthreporting:system"
    value     = "enhanced"
  }

  setting {
    name      = "LOGGING_APPENDER"
    namespace = "aws:elasticbeanstalk:application:environment"
    value     = "GRAYLOG"
  }

  setting {
    name      = "RollingUpdateEnabled"
    namespace = "aws:autoscaling:updatepolicy:rollingupdate"
    value     = "true"
  }

  setting {
    name      = "RollingUpdateType"
    namespace = "aws:autoscaling:updatepolicy:rollingupdate"
    value     = "Health"
  }

  setting {
    name      = "MaxBatchSize"
    namespace = "aws:autoscaling:updatepolicy:rollingupdate"
    value     = "1"
  }

  setting {
    name      = "CrossZone"
    namespace = "aws:elb:loadbalancer"
    value     = "true"
  }

  setting {
    name      = "BatchSizeType"
    namespace = "aws:elasticbeanstalk:command"
    value     = "Fixed"
  }

  setting {
    name      = "StickinessEnabled"
    namespace = "aws:elasticbeanstalk:environment:process:default"
    value     = "true"
  }

  setting {
    name      = "DeploymentPolicy"
    namespace = "aws:elasticbeanstalk:command"
    value     = "Rolling"
  }

  setting {
    name      = "SecurityGroups"
    namespace = "aws:autoscaling:launchconfiguration"
    value     = aws_security_group.vprofile-prod-sg.id
  }

  setting {
    name      = "SecurityGroups"
    namespace = "aws:elbv2:loadbalancer"
    value     = aws_security_group.vprofile-bean-alb-sg.id
  }

  depends_on = [aws_security_group.vprofile-prod-sg, aws_security_group.vprofile-bean-alb-sg]
}
