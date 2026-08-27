# Start Here: project-01-java-aws-3tier

**Learning focus:** Java/Spring Boot application delivery on AWS 3-tier infrastructure with Terraform, Maven,
Tomcat, Nginx, and MySQL

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, inspect the readme headings and the Terraform files locally, then run only the recorded
formatting check `terraform -chdir=terraform fmt -check` without provisioning anything.

## Checkpoints

1. 1. The learner can map the packet's components into frontend Nginx, backend Tomcat, and private MySQL tiers and identify the relevant Terraform files
2. 1. The learner can trace the Java Login App's Maven configuration, JDBC property, JSP pages, and Employee-table schema without changing or deploying them
3. 1. The learner can explain the intended request path from the public Nginx load balancer through the private Tomcat load balancer to the RDS database and cite the packet's validation targets and security boundaries.

## Hints if you are stuck

1. 1. If the local formatting check fails, compare whitespace and Terraform block structure before investigating AWS resources
2. 1. For an application-flow question, follow the `proxy_pass`, target-group, listener, and security-group declarations across the Nginx and Tomcat sections
3. 1. For database-related behavior, compare the JDBC settings, the `UserDB`/`Employee` schema, and the stated private-subnet access sources rather than guessing credentials or network routes.

## Evidence to capture

Annotated local architecture map, formatting-check result, traced Java-to-database configuration, and a short
validation checklist

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
