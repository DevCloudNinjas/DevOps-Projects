provider "aws" {
  region     = "us-east-1"
#  access_key = "my-access-key"
#  secret_key = "my-secret-key"
}

/*====
Get latest AWS credentials
======*/

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = "${data.aws_vpc.default.id}"
}

data "aws_caller_identity" "current" {}

/*===
Security Groups for ALB
====*/

resource "aws_security_group" "lb" {
  name        = "lb-sg"
  description = "controls access to the Application Load Balancer (ALB)"

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs_tasks" {
  name        = "ecs-tasks-sg"
  description = "allow inbound access from the ALB only"

  ingress {
    protocol        = "tcp"
    from_port       = 4000
    to_port         = 4000
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.lb.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

/*====
App Load Balancer
======*/

resource "aws_lb" "staging" {
  name               = "alb"
  subnets            = data.aws_subnet_ids.default.ids
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]

  tags = {
    Environment = "staging"
    Application = "dummyapi"
  }
}

resource "aws_lb_listener" "https_forward" {
  load_balancer_arn = aws_lb.staging.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.staging.arn
  }
}

resource "aws_lb_target_group" "staging" {
  name        = "dummyapi-alb-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = "${aws_vpc.vpc.id}"
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "90"
    protocol            = "HTTP"
    matcher             = "200-299"
    timeout             = "20"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

/*====
ECR repository to store our Docker images
======*/

resource "aws_ecr_repository" "repo" {
  name = "dummyapi/staging/runner"
}

/*====
ECR lifecycle policies
======*/

resource "aws_ecr_lifecycle_policy" "repo-policy" {
  repository = aws_ecr_repository.repo.name

  policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep image deployed with tag latest",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["latest"],
        "countType": "imageCountMoreThan",
        "countNumber": 1
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 2,
      "description": "Keep last 2 any images",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 2
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
}

/*====
IAM service roles and policies
======*/

data "aws_iam_policy_document" "ecs_task_execution_role" {
  version = "2012-10-17"
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "ecs-staging-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

/*====
ECS task definitions
======*/

resource "aws_ecs_task_definition" "service" {
  family                   = "${var.prefix}-task-family"
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  cpu                      = 256
  memory                   = 2048
  requires_compatibilities = ["FARGATE"]
  container_definitions    = templatefile("./app.json.tpl", {
            aws_ecr_repository = aws_ecr_repository.repo.repository_url
            tag                = "latest"
            app_port           = 80
            region             = "${var.region}"
            prefix             = "${var.prefix}"
            envvars            = var.envvars
            port               = var.port
        })
  tags = {
    Environment = "staging"
    Application = "${var.prefix}-app"
  }
}

/*====
ECS service
======*/

resource "aws_ecs_service" "staging" {
  name            = "${var.prefix}-service"
  cluster         = aws_ecs_cluster.staging.id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = data.aws_subnet_ids.default.ids
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.staging.arn
    container_name   = "${var.prefix}-app"
    container_port   = var.port
  }

  depends_on = [aws_lb_listener.https_forward, aws_iam_role_policy_attachment.ecs_task_execution_role]

  tags = {
    Environment = "staging"
    Application = "${var.prefix}-app"
  }
}

/*====
Cloudwatch Log Group
======*/

resource "aws_cloudwatch_log_group" "dummyapi" {
  name = "${var.prefix}-log-group"

  tags = {
    Environment = "staging"
    Application = "${var.prefix}-app"
  }
}

# Replace <AWS_ACCOUNT_ID> with your AWS account ID
// example -> ./push.sh . <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/<IMAGE_NAME> latest

resource "null_resource" "push" {
  provisioner "local-exec" {
    command     = "${coalesce("./push.sh", "${path.module}/push.sh")} ${var.source_path} ${aws_ecr_repository.repo.repository_url} ${var.tag} ${data.aws_caller_identity.current.account_id}"
    interpreter = ["bash", "-c"]
  }
}
