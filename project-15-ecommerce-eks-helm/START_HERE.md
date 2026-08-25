# Start Here: project-15-ecommerce-eks-helm

**Learning focus:** Kubernetes application deployment architecture with Helm, AWS EKS, ALB ingress, and EBS-backed three-tier services

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

In a local copy of the packet, map the README’s presentation, application, and data tiers to the RobotShop Helm chart, `robot-shop` namespace, `ingress.yaml`, and the stated EKS add-ons without running any cloud or deployment command.

## Checkpoints

1. 1. Produce a local dependency map that connects the EKS cluster, IAM/OIDC and load-balancer prerequisites, Helm chart, namespace, pods, and ingress to the three application tiers
2. 2. Annotate the README with the required substitutions and verification points for `cluster_name`, region, VPC ID, AWS account ID, and the RobotShop chart path, while leaving commands unexecuted
3. 3. Submit a local validation checklist showing how successful completion would be recognized from the packet: the `aws-load-balancer-controller` deployment and RobotShop pods would be running, an ingress would expose a load-balancer DNS name, and the application workflow would reach registration, cart, checkout, and order placement.

## Hints if you are stuck

1. 1. If the tier map is unclear, start from the README’s definitions of presentation, application, and data responsibilities before examining the RobotShop chart location
2. 2. Treat every angle-bracket placeholder and each named AWS resource as a value that must be accounted for, not as literal text
3. 3. When a verification point fails in a controlled environment, compare the relevant layer’s prerequisite and namespace/resource name before changing unrelated steps.

## Evidence to capture

Local three-tier dependency map, placeholder/substitution checklist, and ordered verification rubric tied to controller deployment, RobotShop pods, ingress DNS, and checkout flow

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
