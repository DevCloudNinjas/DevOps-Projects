# Start Here: project-38-docker-terraform-3tier

**Learning focus:** Local Docker Compose three-tier Node.js application architecture with Terraform/IaC design

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, review `README.md` and run the packet’s local validation command `docker compose config` without supplying cloud credentials or applying Terraform.

## Checkpoints

1. 1. `docker compose config` parses the three services (`webapp`, `api`, and `db`) and shows the two networks and webapp port mapping
2. 2. The local compose stack builds and starts, with the webapp, API, and PostgreSQL containers reporting running/listening status
3. 3. Visiting `http://localhost:3000` displays the countries-and-capitals table, while the Terraform directory passes `terraform fmt -check` and `terraform validate` without any apply operation.

## Hints if you are stuck

1. 1. If Compose cannot resolve the API or database, compare the service names and attached `network-frontend`/`network-backend` networks with the environment variables in `docker-compose.yml`
2. 2. If the table is empty or the API returns an error, inspect the database container’s initialization output and verify that `init_sql_scripts/init.sql` was mounted as shown
3. 3. If Terraform validation fails, check formatting, required variable declarations, and references among the VPC, subnet, security-group, ALB, EC2, and RDS files before considering any provider interaction.

## Evidence to capture

Local `docker compose config` output, container/status and relevant logs, browser capture of the localhost countries-and-capitals table, and Terraform formatting/validation output

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
