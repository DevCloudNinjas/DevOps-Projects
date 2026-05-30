.PHONY: help quality list-projects validate-project test-tools build-site

PYTHON ?= python3
PROJECT ?=

help:
	@printf '%s\n' \
		'Targets:' \
		'  make quality                         Run tool tests and the repository quality gate' \
		'  make list-projects                   List metadata-discovered root projects' \
		'  make validate-project PROJECT=<path> Validate one project with the quality gate' \
		'  make test-tools                       Run tool unit tests' \
		'  make build-site                       Build the Astro Starlight learning portal'

quality: test-tools
	$(PYTHON) -m tools.quality_gate .

list-projects:
	$(PYTHON) -m tools.list_projects --validate-metadata

validate-project:
	@test -n "$(PROJECT)" || (echo 'PROJECT is required, for example: make validate-project PROJECT=project-31-cloud-native-monitoring' >&2; exit 2)
	$(PYTHON) -m tools.validate_project "$(PROJECT)"

test-tools:
	$(PYTHON) -m pytest tools/tests tools/repo_consolidation/tests -q

build-site:
	npm run build
