#!/bin/bash

# Variables
EC2_IP="your_ec2_public_ip"
EC2_USER="ec2_user"
SSH_KEY="path_to_your_ssh_key.pem"
DOCKER_IMAGE="your_docker_image_name"
DOCKER_CONTAINER_NAME="your_container_name"

# SSH into EC2 instance
ssh -i "$SSH_KEY" "$EC2_USER@$EC2_IP" << EOF

# Pull the latest Docker image
docker pull $DOCKER_IMAGE

# Stop and remove existing container
docker stop $DOCKER_CONTAINER_NAME || true
docker rm $DOCKER_CONTAINER_NAME || true

# Run Docker container
docker run -d --name $DOCKER_CONTAINER_NAME -p 80:80 $DOCKER_IMAGE

EOF