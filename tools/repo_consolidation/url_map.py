"""Static URL mapping registry for old standalone repos → consolidated paths.

Maps every old DevCloudNinjas org repo name to its new location inside
the consolidated ``DevOps-Projects`` repository.  Provides a
case-insensitive lookup function for use by the fixer pipeline.

Requirements: 2.1, 3.1, 9.2
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Static mapping: old repo name  →  consolidated path (relative to repo root)
# ---------------------------------------------------------------------------
# Keys are stored in their *canonical* casing (as they appeared on GitHub).
# Lookup is always case-insensitive — see :func:`lookup`.

URL_MAP: dict[str, str] = {
    # ── Projects 01-30 (original DevOps-Project-XX repos) ─────────────
    # These were originally named "DevOps-Project-XX" and renamed during
    # consolidation.  Some also had standalone repo names.
    "DevOps-Project-01": "project-01-java-aws-3tier",
    "DevOps-Project-02": "project-02-aws-vpc-architecture",
    "DevOps-Project-03": "project-03-linux-fundamentals",
    "DevOps-Project-04": "project-04-django-aws-ecs",
    "DevOps-Project-05": "project-05-docker-jenkins-k8s",
    "DevOps-Project-06": "project-06-advanced-cicd-pipeline",
    "DevOps-Project-07": "project-07-azure-devops-aks-terraform",
    "DevOps-Project-08": "project-08-2048-game-eks",
    "DevOps-Project-09": "project-09-devsecops-netflix-clone",
    "DevOps-Project-10": "project-10-dotnet-azure-devops",
    "DevOps-Project-11": "project-11-aws-2tier-terraform",
    "DevOps-Project-12": "project-12-super-mario-k8s",
    "DevOps-Project-13": "project-13-zomato-clone-devsecops",
    "DevOps-Project-14": "project-14-github-actions-android",
    "DevOps-Project-15": "project-15-ecommerce-eks-helm",
    "DevOps-Project-16": "project-16-jenkins-argocd-k8s",
    "DevOps-Project-17": "project-17-aks-azure-devops",
    "DevOps-Project-18": "project-18-jenkins-java-full-cicd",
    "DevOps-Project-19": "project-19-eks-jenkins-terraform",
    "DevOps-Project-20": "project-20-azure-terraform-pipeline",
    "DevOps-Project-21": "project-21-aws-codepipeline",
    "DevOps-Project-22": "project-22-aws-serverless",
    "DevOps-Project-23": "project-23-swiggy-clone-ecs",
    "DevOps-Project-24": "project-24-dotnet-devsecops",
    "DevOps-Project-25": "project-25-petshop-devsecops",
    "DevOps-Project-26": "project-26-terraform-gitlab-cicd",
    "DevOps-Project-27": "project-27-reddit-eks-argocd",
    "DevOps-Project-28": "project-28-openai-chatbot-eks",
    "DevOps-Project-29": "project-29-voting-app-argocd",
    "DevOps-Project-30": "project-30-blog-app-eks",

    # ── Standalone project repos with their own names ─────────────────
    # These repos had unique names and were merged as new projects 31-49
    # or into existing projects.
    "Zomato-Clone": "project-13-zomato-clone-devsecops",
    "Deployment-of-super-Mario-on-Kubernetes-using-terraform": "project-12-super-mario-k8s",
    "full-stack-blogging-app": "project-30-blog-app-eks",
    "Complete-Kubernetes-DevSecOps-Tetris-Project": "project-32-tetris-devsecops-k8s",
    "cloud-native-monitoring-app": "project-31-cloud-native-monitoring",
    "CI-CD_EKS-GitHub_Actions": "project-33-node-cicd-eks-gha",
    "CICD-With-Terraform-ECS-GH-Actions": "project-34-node-cicd-ecs-terraform-gha",
    "AWS-DevOps_Real-Time_Deployment": "project-36-aws-realtime-deployment",
    "AWS-EKS_Terraform": "project-37-eks-terraform-provision",
    "docker_terraform-three-tier-architecture-master": "project-38-docker-terraform-3tier",
    "github-actions-aws-terraform": "project-39-gha-aws-terraform",
    "kubernetes-dashboard-web-app": "project-40-k8s-dashboard-trivy",
    "Online-Boutique-Assessment": "project-41-online-boutique-microservices",
    "terraform-aws-serverless-rest-api-dynamodb": "project-42-serverless-api-dynamodb",
    "hands_on_scenarios": "project-43-ecs-fargate-terraform",
    "DEVSECOPS-PROJECT-101": "project-44-devsecops-101",
    "DEVOPS_JENKINS_101": "project-45-jenkins-cicd-argocd-vault",
    "deploy-eks-cluster-terraform": "project-46-eks-cluster-terraform-advanced",
    "django-multitenant-saas-ecommerce": "project-47-django-saas-ecommerce",
    "terraform-aws-eks": "project-48-terraform-aws-eks",
    "Text_Encryption_Using_Crypto_Algo_Project": "project-49-text-encryption-cybersecurity",

    # ── E2E repo (merged into project-01) ─────────────────────────────
    "DevOps-Projects-E2E": "project-01-java-aws-3tier",

    # ── Duplicate repos (point to same destination as canonical) ───────
    "Deploy-Zomato-CICD-With-Jenkins-SQ-Trivy": "project-13-zomato-clone-devsecops",
    "Deploying-Super-Mario-on-Kubernetes-using-Terraform": "project-12-super-mario-k8s",
    "Super-Mario-K8s": "project-12-super-mario-k8s",
    "Deploy-Zomato-CICD": "project-13-zomato-clone-devsecops",

    # ── asecguru series (merged into project-35 step folders) ─────────
    "asecguru-1-infra-creation": "project-35-devsecops-pipeline-series/step-1-infra-creation",
    "asecguru-2-sast-sonarcloud": "project-35-devsecops-pipeline-series/step-2-sast-sonarcloud",
    "asecguru-3-sca-snyk": "project-35-devsecops-pipeline-series/step-3-sca-snyk",
    "asecguru-4-docker-ecr": "project-35-devsecops-pipeline-series/step-4-docker-ecr",
    "asecguru-5-deploy-k8s": "project-35-devsecops-pipeline-series/step-5-deploy-k8s",
    "asecguru-6-dast-zap-e2e": "project-35-devsecops-pipeline-series/step-6-dast-zap-e2e",

    # ── Learning resource repos ───────────────────────────────────────
    "devops-bootcamp": "learning/devops-bootcamp",
    "Certified_Kubernetes_Administrator": "learning/kubernetes-cka-prep",
    "kubernetes-learning-path": "learning/kubernetes-learning-path",
    "Kubernetes-Projects-Learning": "learning/kubernetes-projects",
    "kubernetes-projects": "learning/kubernetes-projects",
    "Kubernetes-101": "learning/kubernetes-101",
    "Containers_Fundamental_HandsOn": "learning/containers-fundamentals",
    "Docker_HandsOn_Training": "learning/docker-training",
    "DevOps_101_Projects": "learning/devops-101-track",
    "DevOps_201_Projects": "learning/devops-201-track",
    "DevOps_Random_Projects": "learning/devops-random-projects",
    "Learning-Prometheus": "learning/prometheus-monitoring",
    "Linux-Hands-On": "learning/linux-hands-on",
    "into-the-devops": "learning/devops-interview-prep",
    "sre-interview-prep-guide": "learning/sre-interview-prep",
    "DevOps_Setup-Installations": "learning/tool-setup-guides",

    # ── Resource repos ────────────────────────────────────────────────
    "devops-tools": "resources/devops-tools-list",
    "Github-Examples": "resources/github-actions-examples",
    "coding-interview-university": "resources/coding-interview-university",

    # ── Repos referenced in learning materials ────────────────────────
    # These are app repos referenced in devops-bootcamp docs.
    "dks-ui": "learning/devops-bootcamp",
    "dks-api": "learning/devops-bootcamp",
    "spring-petclinic": "learning/devops-bootcamp",
    "rode": "learning/devops-bootcamp",
    "lead-terraform": "learning/devops-bootcamp",

    # ── Additional repos discovered during dry-run scan ───────────────
    "csgo": "learning/devops-bootcamp",
    "s3-realworld-ui-dob": "learning/devops-bootcamp",
    "microservices-demo": "learning/devops-bootcamp",
    "teamquery": "learning/devops-bootcamp",
    "DevShops": "learning/devops-bootcamp",
}


# ---------------------------------------------------------------------------
# Pre-built case-insensitive index (built once at import time)
# ---------------------------------------------------------------------------

_LOWER_MAP: dict[str, str] = {k.lower(): v for k, v in URL_MAP.items()}


def lookup(repo_name: str) -> str | None:
    """Return the consolidated path for *repo_name*, or ``None`` if unmapped.

    Matching is case-insensitive on the repo name.  For example,
    ``lookup("zomato-clone")`` and ``lookup("Zomato-Clone")`` both
    return ``"project-13-zomato-clone-devsecops"``.
    """
    return _LOWER_MAP.get(repo_name.lower())


def is_mapped(repo_name: str) -> bool:
    """Return ``True`` if *repo_name* has a known mapping."""
    return repo_name.lower() in _LOWER_MAP


# ---------------------------------------------------------------------------
# Consolidated repo constants
# ---------------------------------------------------------------------------

CONSOLIDATED_CLONE_URL = "https://github.com/DevCloudNinjas/DevOps-Projects.git"
CONSOLIDATED_TREE_URL = "https://github.com/DevCloudNinjas/DevOps-Projects/tree/main"


# ---------------------------------------------------------------------------
# Path computation helpers
# ---------------------------------------------------------------------------


def compute_relative_path(from_file: str, to_path: str) -> str:
    """Compute a POSIX-style relative path from *from_file* to *to_path*.

    Both paths are relative to the repo root.  The result is the relative
    path from the **directory containing** *from_file* to *to_path*, using
    forward slashes.

    Examples::

        >>> compute_relative_path("project-13/README.md", "project-30/README.md")
        '../project-30/README.md'
        >>> compute_relative_path("learning/k8s/README.md", "learning/k8s/docs/setup.md")
        'docs/setup.md'
    """
    from pathlib import PurePosixPath

    src_dir = PurePosixPath(from_file).parent
    target = PurePosixPath(to_path)

    # Compute the relative path between the two POSIX paths.
    try:
        rel = target.relative_to(src_dir)
    except ValueError:
        # target is not under src_dir — walk up and across.
        src_parts = src_dir.parts
        tgt_parts = target.parts

        # Find the length of the common prefix.
        common = 0
        for s, t in zip(src_parts, tgt_parts):
            if s == t:
                common += 1
            else:
                break

        ups = len(src_parts) - common
        remainder = tgt_parts[common:]
        rel = PurePosixPath(*([".."] * ups + list(remainder)))

    return str(rel)


def resolve_new_path(old_repo_name: str, old_url: str, source_file: str) -> str | None:
    """Determine the replacement string for *old_url* found in *source_file*.

    Returns ``None`` when *old_repo_name* has no known mapping.

    Context detection:

    * **Clone URL** — the URL contains ``git clone`` or ends with ``.git``
      → return :data:`CONSOLIDATED_CLONE_URL`.
    * **Config metadata** — the URL appears in a ``package.json``
      ``repository`` / ``bugs`` / ``homepage`` field (detected by
      *source_file* name and URL shape)
      → return ``CONSOLIDATED_TREE_URL/{consolidated_path}``.
    * **In-repo reference** (default) — compute a relative path from
      *source_file* to the consolidated path.

    Requirements: 2.1, 2.4, 3.1, 3.5
    """
    consolidated_path = lookup(old_repo_name)
    if consolidated_path is None:
        return None

    # --- Clone URL context ------------------------------------------------
    if old_url.rstrip().endswith(".git") or "git clone" in old_url:
        return CONSOLIDATED_CLONE_URL

    # --- Config metadata context ------------------------------------------
    # package.json repository/bugs/homepage fields use full tree URLs.
    source_lower = source_file.lower()
    _config_files = ("package.json",)
    if any(source_lower.endswith(cf) for cf in _config_files):
        return f"{CONSOLIDATED_TREE_URL}/{consolidated_path}"

    # --- Default: in-repo relative path -----------------------------------
    return compute_relative_path(source_file, consolidated_path)
