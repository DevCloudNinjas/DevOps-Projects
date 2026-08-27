# Start Here: project-29-voting-app-argocd

**Learning focus:** Microservices CI/CD with Docker Compose, Azure DevOps, Kubernetes, and Argo CD

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

Clone the referenced example-voting-app repository into a disposable local directory and inspect its
docker-compose configuration and service directories before starting any containers.

## Checkpoints

1. 1. You can identify the vote, result, worker, Redis, and PostgreSQL services and explain the vote-to-results data flow from the readme
2. 1. The local Compose run starts the application containers and the voting page is reachable at the documented local port 5000
3. 1. After submitting a test vote locally, the results page reflects the vote and you can document which service path connects Redis processing to PostgreSQL-backed results.

## Hints if you are stuck

1. 1. If the Compose startup does not behave as expected, first compare the service names, working directory, and port mapping with the repository's Compose file
2. 1. If the page loads but results do not change, check whether the worker and both data stores are running rather than troubleshooting the browser first
3. 1. For a later pipeline or Argo CD exercise, verify one naming or image-tag value at a time against the repository path and the intended microservice instead of changing every configuration field together.

## Evidence to capture

Annotated local service/data-flow diagram, terminal capture of the Compose services, and screenshots or notes
showing a submitted vote and updated results

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
