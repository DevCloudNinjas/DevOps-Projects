.PHONY: help validate plan up down logs

TF ?= $(shell if command -v tofu >/dev/null 2>&1; then printf tofu; elif command -v terraform >/dev/null 2>&1; then printf terraform; else printf tofu; fi)
PLAN_FILE ?= tfplan

help:
	@printf '%s\n' \
		'Targets:' \
		'  make validate   Format-check and validate IaC locally' \
		'  make plan       Create a reviewable plan file' \
		'  make up         Apply the reviewed plan file' \
		'  make logs       Show outputs from current state' \
		'  make down       Destroy created AWS resources'

validate:
	@test -f main.tf -a -f versions.tf -a -f variables.tf -a -f outputs.tf
	@if command -v $(TF) >/dev/null; then \
		$(TF) fmt -check && \
		$(TF) init -backend=false && \
		$(TF) validate; \
	else \
		echo 'OpenTofu/Terraform not installed; completed file-level validation only.'; \
		echo 'Install OpenTofu or Terraform for fmt, init, and validate checks.'; \
	fi

plan:
	@command -v $(TF) >/dev/null || (echo 'Install OpenTofu or Terraform, then rerun with TF=tofu or TF=terraform' >&2; exit 1)
	$(TF) init
	$(TF) plan -out $(PLAN_FILE)

up:
	@command -v $(TF) >/dev/null || (echo 'Install OpenTofu or Terraform, then rerun with TF=tofu or TF=terraform' >&2; exit 1)
	test -f $(PLAN_FILE) || (echo 'Run make plan before make up so you can review changes first' >&2; exit 1)
	$(TF) apply $(PLAN_FILE)

logs:
	@command -v $(TF) >/dev/null || (echo 'Install OpenTofu or Terraform, then rerun with TF=tofu or TF=terraform' >&2; exit 1)
	$(TF) output

down:
	@command -v $(TF) >/dev/null || (echo 'Install OpenTofu or Terraform, then rerun with TF=tofu or TF=terraform' >&2; exit 1)
	$(TF) destroy
