#makefile for custom terraform provider this is required for terraform plan
.PHONY: testacc clean init plan build generate fmt allCombined provider resource datasource engineer-resource dev-resource ops-resource devops-resource engineer-datasource dev-datasource ops-datasource devops-datasource startbar debug-allCombined

GOOS?=$$(go env GOOS)
GOARCH?=$$(go env GOARCH)

plan: clean init provider resource datasource debug-allCombined

build: main.go generate
	go $@ -o terraform-provider-devops-bootcamp

debug-allCombined:
	terraform -chdir=examples/allCombined init -plugin-dir=../../.plugin-cache
	terraform -chdir=examples/allCombined plan 

startbar:
	@printf "|##                           |\r"

allCombined: startbar init
	@bash .make-helper.sh ac

resource: engineer-resource dev-resource ops-resource devops-resource

datasource: engineer-datasource dev-datasource ops-datasource devops-datasource

generate: main.go
	@go $@ &> /dev/null

fmt: main.tf
	terraform $@

#makes a directory including making gome directories should they not exist (-p)
init: clean build
	@mkdir -p .plugin-cache/devcloudninjas.com/terraform/devops-bootcamp/0.0.1/$(GOOS)_$(GOARCH) && \
	ln -s "${PWD}/terraform-provider-devops-bootcamp" "${PWD}/.plugin-cache/devcloudninjas.com/terraform/devops-bootcamp/0.0.1/$(GOOS)_$(GOARCH)/terraform-provider-devops-bootcamp"

clean: 
	@rm -rf .plugin-cache .terraform .terraform.lock.hcl terraform-provider-devops-bootcamp && \
	rm -rf examples/*/*/.terraform* examples/*/.terraform*

provider:
	terraform -chdir=examples/provider init -plugin-dir=../../.plugin-cache
	terraform -chdir=examples/provider plan

engineer-resource: init
	terraform -chdir=examples/resources/Engineer init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/resources/Engineer plan

dev-resource: init
	terraform -chdir=examples/resources/Dev init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/resources/Dev plan

ops-resource: init
	terraform -chdir=examples/resources/Ops init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/resources/Ops plan

devops-resource: init
	terraform -chdir=examples/resources/DevOps init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/resources/DevOps plan

engineer-datasource: init
	terraform -chdir=examples/data-sources/Engineer init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/data-sources/Engineer plan

dev-datasource: init
	terraform -chdir=examples/data-sources/Dev init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/data-sources/Dev plan

ops-datasource: init
	terraform -chdir=examples/data-sources/Ops init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/data-sources/Ops plan

devops-datasource: init
	terraform -chdir=examples/data-sources/DevOps init -plugin-dir=../../../.plugin-cache/
	terraform -chdir=examples/data-sources/DevOps plan

# Run acceptance tests
testacc:
	TF_ACC=1 go test ./... -v $(TESTARGS) -timeout 120m
