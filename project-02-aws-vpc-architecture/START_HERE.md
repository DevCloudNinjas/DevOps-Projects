# Start Here: project-02-aws-vpc-architecture

**Learning focus:** AWS VPC network architecture and secure cloud application delivery

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

On a local copy, read the main README and sketch the two CIDR blocks, public/private subnet roles, gateways, Transit Gateway, load balancer, and validation stages without creating AWS resources.

## Checkpoints

1. 1. Produce a local architecture sketch that distinguishes the 192.168.0.0/16 bastion VPC from the 172.32.0.0/16 private application VPC and labels the stated gateway and subnet relationships
2. 2. Create a local dependency checklist mapping flow logs, S3 policy/configuration, IAM permissions, launch configuration, Auto Scaling, target group, NLB, and Route 53 to their prerequisite components
3. 3. Assemble a local validation record template covering private-instance access conceptually, Session Manager access, and public web page verification, leaving all live execution for instructor-controlled infrastructure.

## Hints if you are stuck

1. 1. If the architecture sketch is confusing, first separate internet-facing bastion responsibilities from private application-server responsibilities before tracing traffic
2. 2. When a dependency seems missing, compare the requested component with the README's preceding network, identity, logging, and load-balancing steps
3. 3. For a validation mismatch, check whether the evidence corresponds to the stated path—public entry through the NLB, private placement for application instances, and Session Manager rather than SSH to private nodes.

## Evidence to capture

Local two-VPC architecture diagram, dependency checklist, and validation-plan notes tied to the README's stated components

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
