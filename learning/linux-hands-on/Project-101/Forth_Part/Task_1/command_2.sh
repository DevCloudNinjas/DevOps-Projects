#!/bin/bash
PRIVATE_IP=$(grep "PrivateIpAddress" info.json | head -n 1 | sed 's/.*"\(.*\)".*/\1/')
sed '40s/ec2-private_ip/'"$PRIVATE_IP"'/' terraform.tf
