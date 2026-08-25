# Start Here: project-51-opentelemetry-observability-home-lab

**Learning focus:** Local OpenTelemetry observability with traces, metrics, logs, and Grafana LGTM

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project directory, run `make validate` to check the Docker Compose configuration before starting any containers.

## Checkpoints

1. 1. `make validate` completes and reports a valid Compose configuration
2. 2. `make up` starts the local Python app, OpenTelemetry Collector, Prometheus, Tempo, and Grafana services, with the app reachable at `http://localhost:8080`
3. 3. After requesting `/`, `/slow`, and `/error` locally with curl, the resulting telemetry is visible in Grafana Explore or dashboards and can be related to the app requests.

## Hints if you are stuck

1. 1. If validation fails, inspect indentation and the service, port, and volume entries in `docker-compose.yml`
2. 2. If Grafana appears empty, first confirm that local requests have been generated and then refresh Explore or the dashboards
3. 3. If the Collector will not start, use the local logs to check `otel-collector.yaml` and whether its mounted path exists.

## Evidence to capture

Successful `make validate` output, local service status or logs, curl results for the three endpoints, and screenshots or notes showing corresponding traces, metrics, and logs in Grafana.

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
