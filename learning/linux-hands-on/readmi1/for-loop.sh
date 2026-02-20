#/bin/bash

devops_tools=("Kubernetes" "Docker" "Terraform" "Ansible")
devops_tools[5]="Jenkins"

for tool in ${devops_tools[@]}
do
    echo "$tool"
done