#!/bin/bash
set -e

# Check if AWS CLI is installed and configured
if ! command -v aws &> /dev/null; then
  echo "AWS CLI is not installed. Please install it and configure with appropriate permissions."
  exit 1
fi

# Terminate the instance
if aws ec2 terminate-instances --instance-ids $1; then
  echo "Successfully terminated instance $1"
else
  echo "Failed to terminate instance $1"
  exit 1
fi