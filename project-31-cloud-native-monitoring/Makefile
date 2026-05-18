ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif
SHELL := /bin/bash
.DEFAULT_GOAL := help

help:
	@echo "Targets: test lint docker-build"

test:
	@python3 -m unittest discover -s tests

lint:
	@python3 -m py_compile app.py ecr.py eks.py

docker-build:
	@docker build -t cloud-native-monitoring:local .
