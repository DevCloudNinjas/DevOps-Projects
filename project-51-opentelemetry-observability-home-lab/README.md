# Project 51: OpenTelemetry Observability Home Lab

Docker Compose lab for learning traces, metrics, and logs with a small Python app, OpenTelemetry Collector, and Grafana LGTM components.

## What You Learn

- How an app emits telemetry
- What the OpenTelemetry Collector does
- How traces, logs, and metrics fit together
- How to run a local observability stack without cloud cost

## Home Lab Cost

Local only. No cloud account required.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

```bash
docker compose up --build
```

Open:

- App: `http://localhost:8080`
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

Generate traffic:

```bash
curl http://localhost:8080/
curl http://localhost:8080/slow
curl http://localhost:8080/error
```

## Clean Up

```bash
docker compose down -v
```

## Student Exercises

- Add a new endpoint and create a custom span.
- Add a dashboard panel for request count.
- Change the collector pipeline to drop noisy logs.
- Add an alert for repeated `/error` calls.

