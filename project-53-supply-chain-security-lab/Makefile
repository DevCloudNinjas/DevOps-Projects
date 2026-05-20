.PHONY: help validate up logs down scan sbom

IMAGE ?= supply-chain-demo:local
CONTAINER ?= supply-chain-demo

help:
	@printf '%s\n' \
		'Targets:' \
		'  make validate   Run Node syntax check and optional workflow parse' \
		'  make up         Build and run the local demo container' \
		'  make logs       Follow demo container logs' \
		'  make scan       Build, scan, and generate an SBOM' \
		'  make down       Stop and remove the demo container'

validate:
	@command -v node >/dev/null || (echo 'Node.js is required for syntax validation' >&2; exit 1)
	node --check app/server.js
	@python3 -c 'import yaml, pathlib; yaml.safe_load(pathlib.Path(".github/workflows/security.yml").read_text()); print("workflow yaml ok")' 2>/dev/null || echo 'PyYAML not installed; skipped workflow YAML parse'

up:
	@command -v docker >/dev/null || (echo 'Docker is required for make up' >&2; exit 1)
	docker build -t $(IMAGE) app
	docker rm -f $(CONTAINER) >/dev/null 2>&1 || true
	docker run -d --name $(CONTAINER) -p 8080:8080 $(IMAGE)

logs:
	@command -v docker >/dev/null || (echo 'Docker is required for make logs' >&2; exit 1)
	docker logs -f $(CONTAINER)

scan:
	./scripts/local-scan.sh

sbom:
	@command -v syft >/dev/null || (echo 'Syft is required for SBOM generation' >&2; exit 1)
	syft $(IMAGE) -o spdx-json > sbom.spdx.json

down:
	@command -v docker >/dev/null || (echo 'Docker is required for make down' >&2; exit 1)
	docker rm -f $(CONTAINER)
