.PHONY: help validate up logs down

CLUSTER ?= rollout-lab

help:
	@printf '%s\n' \
		'Targets:' \
		'  make validate   Parse namespace, service, and rollout YAML locally' \
		'  make up         Create a Kind cluster and install Argo Rollouts' \
		'  make logs       Show rollout and workload status' \
		'  make down       Delete the Kind cluster'

validate:
	@python3 -c 'import glob, pathlib, yaml; files=glob.glob("rollouts/*.yaml"); [list(yaml.safe_load_all(pathlib.Path(f).read_text())) for f in files]; print("yaml ok:", ", ".join(files))'

up:
	@command -v kind >/dev/null || (echo 'kind is required for make up' >&2; exit 1)
	@command -v kubectl >/dev/null || (echo 'kubectl is required for make up' >&2; exit 1)
	kind create cluster --name $(CLUSTER)
	kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
	kubectl wait --for=condition=available --timeout=180s deployment/argo-rollouts -n argo-rollouts
	kubectl apply -f rollouts/

logs:
	@command -v kubectl >/dev/null || (echo 'kubectl is required for make logs' >&2; exit 1)
	kubectl get rollout,pods,svc -n progressive-delivery

down:
	@command -v kind >/dev/null || (echo 'kind is required for make down' >&2; exit 1)
	kind delete cluster --name $(CLUSTER)
