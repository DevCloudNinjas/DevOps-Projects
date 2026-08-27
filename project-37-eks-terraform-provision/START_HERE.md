# Start Here: project-37-eks-terraform-provision

**Learning focus:** AWS EKS infrastructure-as-code with Terraform: VPC networking, IAM, security groups, and
node-group configuration

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

Open the project locally and trace the Terraform resource references from `vpc.tf`, `subnets.tf`,
`internetgw.tf`, and `rout.tf` into the EKS cluster and node-group files without running `terraform apply`.

## Checkpoints

1. 1. A local dependency map identifies the VPC, two public subnets, internet gateway, route-table associations, security group, IAM roles/policies, EKS cluster, kubectl-server EC2 instance, and EKS node group
2. 1. `terraform fmt -check` and `terraform validate` complete locally after the learner reviews the backend placeholders and variable/default configuration
3. 1. A dry-run plan is inspected locally and the learner can explain the expected EKS cluster, two-node desired capacity, subnet placement, SSH source restriction, and the resources that would incur AWS charges, without applying it.

## Hints if you are stuck

1. 1. If validation or planning reports a backend problem, inspect `eks-backend-terra.tf` for placeholder bucket, key, region, and lock-table values before changing resource definitions
2. 1. If a reference is unresolved, follow the resource name across `vpc.tf`, `subnets.tf`, `iam_role.tf`, `eks_cluster.tf`, and `eks_node_group.tf`, paying attention to hyphenated resource labels
3. 1. If the security review conflicts with the README's safer-default note, compare the active `sg.tf` ingress rule with the documented `admin_cidr_blocks` setting and record the discrepancy rather than widening access.

## Evidence to capture

Local formatted/validated Terraform files, a dependency map or annotated resource graph, and a reviewed
non-applied plan summary with cost and security observations

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
