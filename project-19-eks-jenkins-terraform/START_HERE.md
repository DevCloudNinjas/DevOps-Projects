# Start Here: project-19-eks-jenkins-terraform

**Learning focus:** AWS infrastructure-as-code and Kubernetes CI/CD with Terraform, EKS, and Jenkins

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, open README.md and make a local inventory table mapping each stated stage to its
corresponding Terraform, Jenkins, shell-script, and Kubernetes manifest file without running any commands.

## Checkpoints

1. 1. The learner can point to the files implementing the three infrastructure/application layers: jenkins_server/tf-aws-ec2, tf-aws-eks, and manifest
2. 1. The learner can annotate the README's sequence from Jenkins server provisioning through EKS Terraform validation to Kubernetes application delivery and Jenkins pipeline configuration
3. 1. The learner can produce a local dependency sketch showing that the EC2 bootstrap script supports Jenkins tooling, tf-aws-eks defines the VPC/EKS resources, and the manifest files define the Nginx workload and service.

## Hints if you are stuck

1. 1. If the file-to-stage mapping is unclear, use the active filenames and the readme headings rather than starting with the command examples
2. 1. If Terraform responsibilities seem mixed together, separate the jenkins_server/tf-aws-ec2 directory from tf-aws-eks and inspect their backend, provider, variable, and resource/module files as distinct units
3. 1. If the Kubernetes portion is hard to trace, compare the names and fields in manifest/deployment.yaml and manifest/service.yaml with the example kubectl output, without attempting to connect to a cluster.

## Evidence to capture

Annotated local architecture/dependency map plus a stage-to-file inventory and a short explanation of the
Terraform, Jenkins, and Kubernetes handoffs

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
