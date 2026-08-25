# Start Here: project-48-terraform-aws-eks

**Learning focus:** Terraform/OpenTofu infrastructure-as-code for AWS EKS and Kubernetes workloads

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

In a disposable local copy, inventory the Terraform and Kubernetes manifests and run `terraform fmt -check` without initializing, applying, or contacting AWS.

## Checkpoints

1. 1. The learner can label the Terraform files by responsibility—VPC/subnets/routing, EKS/node groups, provider/variables/outputs—and identify `terraform.tfvars.example` as configuration input
2. 2. The learner can explain from the architecture and manifests that private worker nodes run the Laravel/MySQL workload while a Kubernetes LoadBalancer Service provides the external application path, without deploying it
3. 3. The learner can produce local validation evidence showing formatting and configuration concerns, including the public API CIDR default, secret-template separation, resource probes/limits, and the need for IaC security scanning before any apply.

## Hints if you are stuck

1. 1. If the Terraform inventory feels confusing, trace the variable and resource references from `provider.tf` and `variables.tf` into the VPC, subnet, node-group, and EKS files rather than reading files in filename order
2. 2. If the Kubernetes manifests are unclear, compare the labels/selectors, container ports, probes, and secret references across `db-secret.template.yaml`, `deployment.yaml`, and `service.yaml`
3. 3. If a security concern is missed, review the runbook's Security Notes and ask whether an API allow list, private-subnet placement, encryption, and secret handling are demonstrably constrained before treating the design as ready.

## Evidence to capture

Annotated local architecture/file map, read-only validation output, and a short security-and-workload review identifying the API CIDR, secret workflow, node placement, and service exposure

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
