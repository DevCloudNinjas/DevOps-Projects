[
    {
      "name": "${prefix}-app",
      "image": "${aws_ecr_repository}:${tag}",
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-region": "${region}",
          "awslogs-stream-prefix": "${prefix}-service",
          "awslogs-group": "${prefix}-log-group"
        }
      },
      "portMappings": [
        {
          "containerPort": ${port},
          "hostPort": ${port},
          "protocol": "tcp"
        }
      ],
      "cpu": 1,
      "environment": [
        %{ for env_key, env_value in envvars }
        {
          "name": "${env_key}",
          "value": "${env_value}"
        },
        %{ endfor ~}
        {
          "name": "NODE_ENV",
          "value": "staging"
        },
        {
          "name": "PORT",
          "value": "${port}"
        }
      ],
      "ulimits": [
        {
          "name": "nofile",
          "softLimit": 65536,
          "hardLimit": 65536
        }
      ],
      "mountPoints": [],
      "memory": 2048,
      "volumesFrom": []
    }
  ]