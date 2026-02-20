# Creating Elastic Container Repository for application
resource "aws_ecr_repository" "flask_app" {
  name = "${var.ecr_repo_name}-${var.environment}"
}

# Internet Access -> IGW ->  Route Table -> Subnets
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "My VPC"
  }
}

resource "aws_subnet" "public_subnet_a" {
  availability_zone = "us-east-1a"
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.0.0/24"
  tags = {
    Name = "Public Subnet A"
  }
}

resource "aws_subnet" "public_subnet_b" {
  availability_zone = "us-east-1b"
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.1.0/24"
  tags = {
    Name = "Public Subnet B"
  }
}

resource "aws_subnet" "public_subnet_c" {
  availability_zone = "us-east-1c"
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.2.0/24"
  tags = {
    Name = "Public Subnet C"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name = "My VPC - Internet Gateway"
  }
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.my_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "Public Subnet Route Table"
  }
}

resource "aws_route_table_association" "route_table_association1" {
  subnet_id      = aws_subnet.public_subnet_a.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_route_table_association" "route_table_association2" {
  subnet_id      = aws_subnet.public_subnet_b.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_route_table_association" "route_table_association3" {
  subnet_id      = aws_subnet.public_subnet_c.id
  route_table_id = aws_route_table.route_table.id
}

# Getting data existed ECR
data "aws_ecr_repository" "flask_app" {
  name = "flask-application"
  depends_on = [ aws_ecr_repository.flask_app ]
}

# Creating ECS Cluster
resource "aws_ecs_cluster" "my_cluster" {
  name = "my-cluster" # Naming the cluster
}

# Creating ECS Task
resource "aws_ecs_task_definition" "flask_app_task" {
  family                   = "flask-app-task"
  container_definitions    = <<DEFINITION
  [
    {
      "name": "flask-app-task",
      "image": "${data.aws_ecr_repository.flask_app.repository_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"] # Stating that we are using ECS Fargate
  network_mode             = "awsvpc"    # Using awsvpc as our network mode as this is required for Fargate
  memory                   = 512         # Specifying the memory our container requires
  cpu                      = 256         # Specifying the CPU our container requires
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
}

# Creating Role for ECS
resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# Role - Policy Attachment for ECS
resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Internet Access -> IGW -> LB Security Groups -> Application Load Balancer  (Listener 80) -> Target Groups  -> ECS Service -> ECS SG -> Tasks on each subnets 

# Creating Load Balancer (LB)
resource "aws_alb" "application_load_balancer" {
  name               = "test-lb-tf" # Naming our load balancer
  load_balancer_type = "application"
  subnets = [
    "${aws_subnet.public_subnet_a.id}",
    "${aws_subnet.public_subnet_b.id}",
    "${aws_subnet.public_subnet_c.id}"
  ]
  # Referencing the security group
  security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
}

# Creating a security group for LB
resource "aws_security_group" "load_balancer_security_group" {
  vpc_id = aws_vpc.my_vpc.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic in from all sources
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Creating LB Target Group
resource "aws_lb_target_group" "target_group" {
  name        = "target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.my_vpc.id
}

# Creating LB Listener
resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.application_load_balancer.arn # Referencing our load balancer
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn # Referencing our target group
  }
}

# Creating ECS Service
resource "aws_ecs_service" "my_first_service" {
  name            = "my-first-service"                         # Naming our first service
  cluster         = aws_ecs_cluster.my_cluster.id              # Referencing our created Cluster
  task_definition = aws_ecs_task_definition.flask_app_task.arn # Referencing the task our service will spin up
  launch_type     = "FARGATE"
  desired_count   = 3 # Setting the number of containers to 3

  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn # Referencing our target group
    container_name   = aws_ecs_task_definition.flask_app_task.family
    container_port   = 5000 # Specifying the container port
  }

  network_configuration {
    subnets          = ["${aws_subnet.public_subnet_a.id}", "${aws_subnet.public_subnet_b.id}", "${aws_subnet.public_subnet_c.id}"]
    assign_public_ip = true                                                # Providing our containers with public IPs
    security_groups  = ["${aws_security_group.service_security_group.id}"] # Setting the security group
  }
}

# Creating SG for ECS Container Service, referencing the load balancer security group
resource "aws_security_group" "service_security_group" {
  vpc_id = aws_vpc.my_vpc.id
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    # Only allowing traffic in from the load balancer security group
    security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}