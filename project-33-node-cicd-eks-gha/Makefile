ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif
SHELL := /bin/bash
.DEFAULT_GOAL := help

help:
	@echo "Targets: test lint kustomize-build docker-build"

test:
	@cd app && npm test -- --runInBand

lint:
	@cd app && npm run lint

kustomize-build:
	@kubectl kustomize kustomize/base >/dev/null
	@kubectl kustomize kustomize/overlays/dev >/dev/null
	@kubectl kustomize kustomize/overlays/staging >/dev/null
	@kubectl kustomize kustomize/overlays/prod >/dev/null

docker-build:
	@docker build -t node-cicd-eks-gha:local app
