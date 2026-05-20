.PHONY: help validate up logs down

help:
	@printf '%s\n' \
		'Targets:' \
		'  make validate   Validate docker compose configuration' \
		'  make up         Start the local observability stack' \
		'  make logs       Follow app and collector logs' \
		'  make down       Stop containers and remove lab volumes'

validate:
	@command -v docker >/dev/null || (echo 'Docker is required for compose validation' >&2; exit 1)
	docker compose config

up:
	@command -v docker >/dev/null || (echo 'Docker is required for make up' >&2; exit 1)
	docker compose up --build -d

logs:
	@command -v docker >/dev/null || (echo 'Docker is required for make logs' >&2; exit 1)
	docker compose logs -f app otel-collector

down:
	@command -v docker >/dev/null || (echo 'Docker is required for make down' >&2; exit 1)
	docker compose down -v
