# RDS MySQL Instance
resource "aws_db_subnet_group" "mysql" {
  name       = "mysql-subnet-group"
  subnet_ids = [aws_subnet.app_private_subnet.id, aws_subnet.app_public_subnet.id]
}

resource "aws_db_instance" "mysql" {
  identifier             = "myapp-mysql"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.medium"
  allocated_storage      = 20
  storage_type           = "gp2"
  multi_az               = true
  db_name                = "myapp"
  username               = "admin"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.mysql.name
  vpc_security_group_ids = [aws_security_group.mysql_sg.id]
  skip_final_snapshot    = true
}

resource "aws_security_group" "mysql_sg" {
  name        = "mysql-sg"
  description = "Security group for MySQL RDS"
  vpc_id      = aws_vpc.app_vpc.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.bastion_vpc.cidr_block, aws_vpc.app_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
