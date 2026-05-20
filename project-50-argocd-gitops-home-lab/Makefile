.PHONY: help validate up logs down

CLUSTER ?= gitops-lab

help:
	@printf '%s\n' \
		'Targets:' \
		'  make validate   Parse Kubernetes and ArgoCD YAML locally' \
		'  make up         Create a Kind cluster and install ArgoCD' \
		'  make logs       Show ArgoCD application and workload status' \
		'  make down       Delete the Kind cluster'

validate:
	@python3 -c 'import glob, pathlib, yaml; files=glob.glob("k8s/*.yaml")+glob.glob("argocd/*.yaml"); [list(yaml.safe_load_all(pathlib.Path(f).read_text())) for f in files]; print("yaml ok:", ", ".join(files))'

up:
	@command -v kind >/dev/null || (echo 'kind is required for make up' >&2; exit 1)
	@command -v kubectl >/dev/null || (echo 'kubectl is required for make up' >&2; exit 1)
	kind create cluster --name $(CLUSTER)
	kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
	kubectl wait --for=condition=available --timeout=180s deployment/argocd-server -n argocd
	kubectl apply -f argocd/application.yaml

logs:
	@command -v kubectl >/dev/null || (echo 'kubectl is required for make logs' >&2; exit 1)
	kubectl get applications -n argocd
	kubectl get pods,svc -n gitops-demo

down:
	@command -v kind >/dev/null || (echo 'kind is required for make down' >&2; exit 1)
	kind delete cluster --name $(CLUSTER)
