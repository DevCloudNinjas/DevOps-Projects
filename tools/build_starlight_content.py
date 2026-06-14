"""Generate Astro Starlight content from the repository docs and projects."""

from __future__ import annotations

import json
import posixpath
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

try:  # PyYAML is available locally, but Vercel's build image may not include it.
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised in Vercel build only
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DOCS = REPO_ROOT / "docs"
TARGET_DOCS = REPO_ROOT / "src" / "content" / "docs"
SITE_BASE = "/" if os.environ.get("VERCEL") in {"1", "true"} else "/DevOps-Projects"
GITHUB_REPO = "https://github.com/DevCloudNinjas/DevOps-Projects"
GITHUB_TREE = f"{GITHUB_REPO}/tree/master"
GITHUB_BLOB = f"{GITHUB_REPO}/blob/master"
GITHUB_RAW = "https://raw.githubusercontent.com/DevCloudNinjas/DevOps-Projects/master"
PORTAL_LAST_REVIEWED = "2026-05-30"
START_ROUTES = [
    {
        "label": "I am new to DevOps",
        "href": "/learning-paths/beginner/",
        "title": "Beginner route",
        "summary": "Start with Linux, shell, simple delivery, and a low-risk local lab.",
        "proof": "You will leave with commands, screenshots, and a first portfolio note.",
    },
    {
        "label": "I know Docker/Kubernetes",
        "href": "/learning-paths/docker-kubernetes/",
        "title": "Containers and clusters",
        "summary": "Practice Docker packaging, Kubernetes manifests, services, GitOps, and canary delivery.",
        "proof": "You will prove the work with running pods, service output, and cleanup evidence.",
    },
    {
        "label": "I want AWS/Terraform",
        "href": "/learning-paths/terraform-iac/",
        "title": "AWS and infrastructure as code",
        "summary": "Move through Terraform, OpenTofu, VPCs, ECS, EKS, serverless, and destroy habits.",
        "proof": "You will capture plans, apply output, tagged resources, and destroy confirmation.",
    },
    {
        "label": "I want DevSecOps",
        "href": "/learning-paths/devsecops/",
        "title": "Security in delivery",
        "summary": "Learn scanning, SBOMs, signing, secrets hygiene, and secure pipeline gates.",
        "proof": "You will collect scan output, signed artifacts, and policy evidence.",
    },
    {
        "label": "I want portfolio projects",
        "href": "/flagship/",
        "title": "Flagship portfolio projects",
        "summary": "Pick stronger capstones with cloud, CI/CD, Kubernetes, and production-style proof.",
        "proof": "You will produce a short case study, architecture notes, and validation screenshots.",
    },
]
TOOL_LABELS = {
    "argocd": "Argo CD",
    "aws": "AWS",
    "azure": "Azure",
    "azure-devops": "Azure DevOps",
    "api-gateway": "API Gateway",
    "aks": "AKS",
    "aws-codepipeline": "AWS CodePipeline",
    "clone-app": "Clone App",
    "codebuild": "CodeBuild",
    "codedeploy": "CodeDeploy",
    "codepipeline": "CodePipeline",
    "dynamodb": "DynamoDB",
    "game-deployment": "Game Deployment",
    "docker-compose": "Docker Compose",
    "ci/cd": "CI/CD",
    "ecr": "ECR",
    "ecs": "ECS",
    "eks": "EKS",
    "html": "HTML",
    "github-actions": "GitHub Actions",
    "gitlab-ci": "GitLab CI",
    "linux-scripts": "Linux Scripts",
    ".net": ".NET",
    "net": ".NET",
    "mysql": "MySQL",
    "node-js": "Node.js",
    "nodejs": "Node.js",
    "opentofu": "OpenTofu",
    "route53": "Route 53",
    "sam": "SAM",
    "sonarqube": "SonarQube",
    "terraform": "Terraform",
    "jenkins": "Jenkins",
    "kubernetes": "Kubernetes",
    "monitoring": "Monitoring",
    "nginx": "Nginx",
    "python": "Python",
    "spring-boot": "Spring Boot",
    "vpc": "VPC",
    "vpc-design": "VPC design",
}


def unique_items(*groups: list[str]) -> list[str]:
    seen: set[str] = set()
    items: list[str] = []
    for group in groups:
        for item in group:
            display = display_tool(item)
            key = re.sub(r"[^a-z0-9]+", "", display.lower())
            if key and key not in seen:
                seen.add(key)
                items.append(display)
    return items


def display_tool(item: str) -> str:
    stripped = item.strip()
    lowered = stripped.lower()
    normalized = re.sub(r"[\s_]+", "-", lowered)
    label = TOOL_LABELS.get(lowered) or TOOL_LABELS.get(normalized)
    if label:
        return label

    words = [part for part in re.split(r"[-_/\s]+", stripped) if part]
    if not words:
        return stripped

    def humanize_word(word: str) -> str:
        lower = word.lower()
        if lower == "html":
            return "HTML"
        if lower == "mysql":
            return "MySQL"
        if lower in {"aws", "eks", "ecs", "ecr", "ec2", "vpc", "iam", "rds", "sns", "sqs", "elb", "alb", "nlb"}:
            return lower.upper()
        if lower == "cd":
            return "CD"
        if lower == "devops":
            return "DevOps"
        if lower == "devsecops":
            return "DevSecOps"
        if lower == "opentelemetry":
            return "OpenTelemetry"
        if lower == "opentofu":
            return "OpenTofu"
        if lower == "node":
            return "Node"
        return lower.capitalize()

    display = " ".join(humanize_word(word) for word in words)
    return display.replace("Node Js", "Node.js")


def parse_scalar(value: str) -> object:
    if not value:
        return ""
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value == "[]":
        return []
    return value


def parse_project_yaml(text: str) -> dict:
    if yaml is not None:
        return yaml.safe_load(text)

    data: dict[str, object] = {}
    section: dict[str, object] | None = None
    list_key: str | None = None

    for line_number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip(" "))

        if list_key is not None:
            if stripped.startswith("- "):
                assert isinstance(data[list_key], list)
                data[list_key].append(parse_scalar(stripped[2:].strip()))
                continue
            if indent == 0:
                list_key = None
            else:
                raise ValueError(f"Unexpected nested line at {line_number}: {stripped}")

        if indent == 0:
            if ":" not in stripped:
                raise ValueError(f"Malformed line {line_number}: {stripped}")
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()

            section = None
            if value:
                data[key] = parse_scalar(value)
            elif key in {"stack", "cloud", "iac", "ci_cd"}:
                data[key] = []
                list_key = key
            else:
                data[key] = {}
                section = data[key]  # type: ignore[assignment]
            continue

        if section is None:
            raise ValueError(f"Unexpected indented line {line_number}: {stripped}")
        if ":" not in stripped:
            raise ValueError(f"Malformed nested line {line_number}: {stripped}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        section[key] = parse_scalar(value)

    return data


def project_tools(project: dict) -> list[str]:
    return unique_items(
        project.get("stack", []),
        project.get("cloud", []),
        project.get("iac", []),
        project.get("ci_cd", []),
    )


def skill_level(project: dict) -> str:
    tools = {tool.lower() for tool in project_tools(project)}
    name = f"{project['name']} {project['slug']}".lower()
    if project["cost_risk"] == "high" or "advanced" in name or {"eks", "aks"} & tools:
        return "Advanced"
    if (
        project["cost_risk"] == "medium"
        or project["cloud"]
        or project["iac"]
        or project["ci_cd"]
        or project["deployability"]
        in {"container_ready", "kubernetes_ready", "iac_ready", "ci_cd_ready"}
    ):
        return "Intermediate"
    return "Beginner"


def time_estimate(project: dict, level: str) -> str:
    if project["deployability"] == "reference_only":
        return "30-60 min"
    if level == "Advanced":
        return "3-5 hours"
    if level == "Intermediate":
        return "2-3 hours"
    if project["deployability"] in {"local_only", "container_ready"}:
        return "60-90 min"
    return "90-120 min"


def works_locally(project: dict) -> str:
    return "No" if project["cloud"] else "Yes"


def needs_cloud_credentials(project: dict) -> str:
    return "Yes" if project["cloud"] else "No"


def cleanup_available(project: dict, readme_text: str) -> str:
    cleanup_words = r"\b(clean\s?up|cleanup|destroy|teardown|delete|remove)\b"
    if re.search(cleanup_words, readme_text, flags=re.IGNORECASE):
        return "Yes"
    if not project["cloud"] and project["cost_risk"] == "low":
        return "Yes"
    return "No"


def outcome_proof(project: dict) -> str:
    deployability = project["deployability"]
    if deployability == "reference_only":
        return "Architecture notes plus validation output"
    if deployability == "iac_ready":
        return "Plan/apply evidence plus destroy proof"
    if deployability == "ci_cd_ready":
        return "Passing pipeline run plus scan/deploy evidence"
    if deployability == "kubernetes_ready":
        return "Kubernetes resource output plus app/GitOps screenshot"
    if deployability == "container_ready":
        return "Running container/app screenshot plus logs"
    if deployability == "local_only":
        return "Local output screenshot plus cleanup proof"
    return "Validation command output plus learning notes"


def lab_metadata(project: dict, readme_text: str) -> dict[str, str | list[str]]:
    level = skill_level(project)
    tools = project_tools(project)
    return {
        "skill_level": level,
        "time_estimate": time_estimate(project, level),
        "tools": tools,
        "outcome_proof": outcome_proof(project),
        "cleanup_available": cleanup_available(project, readme_text),
        "last_reviewed": PORTAL_LAST_REVIEWED,
        "works_locally": works_locally(project),
        "needs_cloud_credentials": needs_cloud_credentials(project),
    }


def load_projects() -> list[dict]:
    projects: list[dict] = []
    for metadata_path in sorted(REPO_ROOT.glob("project-*/project.yaml")):
        project_dir = metadata_path.parent
        metadata = parse_project_yaml(metadata_path.read_text(encoding="utf-8"))
        readme_path = project_dir / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8")
        project = metadata["project"]
        number = int(project["number"])
        slug = project["slug"]
        route = f"{number:02d}-{slug}"
        item = {
            "number": number,
            "slug": slug,
            "route": route,
            "dir": project_dir.name,
            "name": project["name"],
            "classification": metadata["classification"],
            "status": metadata["status"],
            "deployability": metadata["deployability"],
            "stack": metadata.get("stack", []),
            "cloud": metadata.get("cloud", []),
            "iac": metadata.get("iac", []),
            "ci_cd": metadata.get("ci_cd", []),
            "cost_risk": metadata["cost_risk"],
            "security_posture": metadata["security_posture"],
            "validation": metadata["validation"]["command"],
            "notes": metadata["notes"],
            "readme": readme_path,
        }
        item.update(lab_metadata(item, readme_text))
        projects.append(item)
    return sorted(projects, key=lambda item: item["number"])


def project_maps(projects: list[dict]) -> tuple[dict[str, str], dict[str, dict]]:
    by_dir = {
        project["dir"]: site_path(f"/projects/{project['route']}/")
        for project in projects
    }
    by_route = {project["route"]: project for project in projects}
    return by_dir, by_route


def site_path(path: str) -> str:
    if path.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return path
    normalized = path if path.startswith("/") else f"/{path}"
    if SITE_BASE == "/":
        return normalized
    if normalized == SITE_BASE or normalized.startswith(f"{SITE_BASE}/"):
        return normalized
    return f"{SITE_BASE}{normalized}"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip()
    return text


def page_title(path: Path, body: str) -> str:
    heading = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    if heading:
        return re.sub(r"\s+", " ", heading.group(1)).strip()
    if path.name == "index.md":
        return path.parent.name.replace("-", " ").title() or "Home"
    return path.stem.replace("-", " ").title()


def frontmatter(
    title: str, order: int | None = None, description: str | None = None
) -> str:
    lines = ["---", f"title: {json.dumps(title)}"]
    if description:
        lines.append(f"description: {json.dumps(description)}")
    if order is not None:
        lines.extend(["sidebar:", f"  order: {order}"])
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def rewrite_site_links(
    text: str, project_link_map: dict[str, str], source_relative: Path
) -> str:
    for project_dir, internal_url in project_link_map.items():
        text = text.replace(f"{GITHUB_TREE}/{project_dir}", internal_url)
        text = text.replace(f"{GITHUB_REPO}/tree/master/{project_dir}", internal_url)
        text = text.replace(
            f"https://github.com/devcloudninjas/DevOps-Projects/tree/master/{project_dir}",
            internal_url,
        )
        text = re.sub(
            rf"(?<![\w/-]){re.escape(project_dir)}(?=/|\))",
            internal_url.rstrip("/"),
            text,
        )

    text = re.sub(r"\.html(?=[)#\"'\s])", "/", text)
    text = text.replace("../learning-paths/", "/learning-paths/")
    text = text.replace("../runbooks/", "/runbooks/")
    text = text.replace("../catalog/", "/catalog/")
    text = text.replace("../security-baselines/", "/security-baselines/")
    text = text.replace("../community/", "/community/")
    text = rewrite_markdown_doc_links(text, source_relative)
    return prefix_root_internal_links(text)


def rewrite_markdown_doc_links(text: str, source_relative: Path) -> str:
    doc_link = re.compile(
        r'(?P<prefix>\]\(|href=")'
        r'(?P<target>(?!https?://|mailto:|tel:|#)[^)"\s]+?\.md)'
        r'(?P<anchor>#[^)"\s]*)?'
        r'(?P<suffix>[\s)"])'
    )

    def replace(match: re.Match[str]) -> str:
        target = match.group("target")
        if target.startswith(f"{SITE_BASE}/"):
            doc_path = target[len(SITE_BASE) + 1 :]
        elif target.startswith("/"):
            doc_path = target.lstrip("/")
        else:
            doc_path = posixpath.normpath((source_relative.parent / target).as_posix())

        route = doc_path.removesuffix(".md")
        if route.endswith("/index"):
            route = route[: -len("/index")]
        href = site_path(f"/{route}/")
        if match.group("anchor"):
            href += match.group("anchor")
        return f"{match.group('prefix')}{href}{match.group('suffix')}"

    return doc_link.sub(replace, text)


def prefix_root_internal_links(text: str) -> str:
    root_link = re.compile(
        r'(?P<prefix>\]\(|href="|src=")/'
        rf"(?!{re.escape(SITE_BASE).lstrip('/')}(?:/|$)|_astro/|pagefind/|favicon\.svg)"
        r'(?P<target>[^)"\s]*)(?P<suffix>[\s)"])'
    )

    def replace(match: re.Match[str]) -> str:
        return (
            f"{match.group('prefix')}"
            f"{site_path('/' + match.group('target'))}"
            f"{match.group('suffix')}"
        )

    return root_link.sub(replace, text)


def rewrite_project_readme_links(text: str, project_dir: str) -> str:
    text = rewrite_github_readme_anchors(text, project_dir)
    text = normalize_code_fence_languages(text)

    def replace_image(match: re.Match[str]) -> str:
        alt, raw_target = match.group(1), match.group(2)
        target, title = split_markdown_destination(raw_target)
        target = normalize_external_image_url(target)
        if is_external_or_anchor(target):
            if target.startswith("#"):
                return f"![{alt}]({target}{title})"
            return external_image_reference(alt, target)
        source_path, _ = repo_source_path(project_dir, target)
        raw_path = quote(source_path, safe="/:@")
        return f"![{alt}]({GITHUB_RAW}/{raw_path}{title})"

    def replace_link(match: re.Match[str]) -> str:
        label, raw_target = match.group(1), match.group(2)
        target, title = split_markdown_destination(raw_target)
        if is_external_or_anchor(target):
            if is_same_repo_source_url(target, project_dir):
                return f"[{label}](#source-files-on-github)"
            if target.startswith(("http://", "https://")):
                return external_link(label, target)
            return match.group(0)
        source_path, fragment = repo_source_path(project_dir, target)
        if source_path.lower() in {f"{project_dir}/readme.md", "readme.md", ""}:
            anchor = f"#{fragment}" if fragment else "#_top"
            return f"[{label}]({anchor})"
        return f"[{label}](#source-files-on-github)"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, text)
    text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
    text = rewrite_bare_github_urls(text)
    return text


def normalize_code_fence_languages(text: str) -> str:
    return text.replace("```bashgo", "```bash").replace("```groocy", "```groovy")


def split_markdown_destination(raw_target: str) -> tuple[str, str]:
    target = raw_target.strip()
    title = ""
    quoted = re.match(r"^(?P<target><[^>]+>|\S+)(?P<title>\s+['\"].*['\"])\s*$", target)
    if quoted:
        target = quoted.group("target")
        title = quoted.group("title")
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target, title


def repo_source_path(project_dir: str, target: str) -> tuple[str, str]:
    parsed = urlsplit(target)
    path = unquote(parsed.path)
    source_path = path.lstrip("/") if path.startswith("/") else f"{project_dir}/{path}"
    source_path = posixpath.normpath(source_path)
    return source_path, parsed.fragment


def rewrite_github_readme_anchors(text: str, project_dir: str) -> str:
    readme_url = re.escape(f"{GITHUB_BLOB}/{project_dir}/README.md")
    return re.sub(readme_url + r"#([A-Za-z0-9_.-]+)", r"#\1", text)


def is_external_or_anchor(target: str) -> bool:
    lower = target.lower()
    return (
        lower.startswith(("http://", "https://", "mailto:", "tel:", "#"))
        or "://" in lower
    )


def normalize_external_image_url(target: str) -> str:
    parsed = urlsplit(target)
    if parsed.netloc.lower() == "imgur.com" and re.search(
        r"\.(png|jpe?g|gif|webp)$", parsed.path, flags=re.IGNORECASE
    ):
        return f"https://i.imgur.com{parsed.path}"
    return target


def external_image_reference(alt: str, target: str) -> str:
    label = alt.strip() or "Source image"
    return (
        '\n<div class="external-image-reference">\n'
        "  <strong>External image reference</strong>\n"
        f'  <a href="{escape_html(target)}" target="_blank" '
        f'rel="noopener noreferrer">{escape_html(label)}</a>\n'
        "</div>\n"
    )


def external_link(label: str, target: str) -> str:
    return (
        f'<a href="{escape_html(target)}" target="_blank" '
        f'rel="noopener noreferrer">{escape_html(label)}</a>'
    )


def rewrite_bare_github_urls(text: str) -> str:
    bare_github_url = re.compile(r'(?<!href=")(?<!\()https://github\.com/[^\s<>"\']+')
    parts = re.split(r"(```.*?```)", text, flags=re.DOTALL)
    for index, part in enumerate(parts):
        if part.startswith("```"):
            continue
        parts[index] = bare_github_url.sub(
            lambda match: external_link("GitHub source link", match.group(0)),
            part,
        )
    return "".join(parts)


def is_same_repo_source_url(target: str, project_dir: str) -> bool:
    parsed = urlsplit(target)
    host = parsed.netloc.lower()
    path = unquote(parsed.path).lower()
    project_prefixes = (
        f"/devcloudninjas/devops-projects/blob/master/{project_dir.lower()}",
        f"/devcloudninjas/devops-projects/tree/master/{project_dir.lower()}",
        f"/devcloudninjas/devops-projects/blob/main/{project_dir.lower()}",
        f"/devcloudninjas/devops-projects/tree/main/{project_dir.lower()}",
    )
    if host == "github.com":
        return path.startswith(project_prefixes)
    if host == "raw.githubusercontent.com":
        return path.startswith(
            f"/devcloudninjas/devops-projects/master/{project_dir.lower()}"
        ) or path.startswith(
            f"/devcloudninjas/devops-projects/main/{project_dir.lower()}"
        )
    return False


def strip_first_h1(text: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", text, count=1, flags=re.MULTILINE).lstrip()


def original_readme_anchor(text: str) -> str:
    heading = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if not heading:
        return ""
    anchor = github_heading_slug(heading.group(1))
    if not anchor:
        return ""
    return f'<span id="{escape_html(anchor)}" class="source-heading-anchor" aria-hidden="true"></span>\n\n'


def github_heading_slug(text: str) -> str:
    plain = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
    plain = re.sub(r"<[^>]+>", "", plain)
    plain = re.sub(r"[`*_~]", "", plain)
    plain = plain.encode("ascii", "ignore").decode("ascii").lower()
    plain = re.sub(r"[^a-z0-9\s-]", "", plain)
    plain = re.sub(r"\s+", "-", plain.strip())
    return plain


def tag_slug(tag: str) -> str:
    slug = display_tool(tag).strip().lower()
    slug = slug.replace("&", " and ")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def tag_href(tag: str) -> str:
    return site_path(f"/tags/{tag_slug(tag)}/")


def demote_markdown_headings(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        level = min(len(match.group(1)) + 3, 6)
        return f"{'#' * level}{match.group(2)}"

    return re.sub(r"^(#{1,5})(\s+)", replace, text, flags=re.MULTILINE)


def write_homepage(projects: list[dict]) -> None:
    featured_numbers = {50, 51, 52, 53, 54}
    featured = [
        project for project in projects if project["number"] in featured_numbers
    ]
    featured_cards = "\n".join(project_card(project) for project in featured)
    start_cards = "\n".join(start_route_card(route) for route in START_ROUTES)
    hero_routes = "\n".join(hero_route_link(route) for route in START_ROUTES)
    content = f"""---
title: DevOps Projects Student Portal
description: A clean DevOps learning portal with internal project pages, guided paths, and safety-first runbooks.
---

<section class="hero-lab">
  <div class="hero-copy">
    <p class="eyebrow">2026 DevOps portfolio lab</p>
    <h1>Build DevOps labs at home. Show the proof.</h1>
    <div class="hero-lede">
      A student-first portal for 54 hands-on DevOps projects across cloud,
      containers, Kubernetes, CI/CD, DevSecOps, observability, and platform
      engineering.
    </div>
    <div class="hero-actions">
      <a class="portal-button primary" href="{site_path('/catalog/start-here/')}">Start here</a>
      <a class="portal-button secondary" href="{site_path('/projects/')}">Browse projects</a>
      <a class="portal-button" href="{site_path('/runbooks/credentials-and-cost-safety/')}">Read the safety guide</a>
    </div>
  </div>
  <div class="hero-metrics" aria-label="Start routes">
    <p class="hero-panel-label">Choose your route</p>
    <div class="hero-route-list">
{hero_routes}
    </div>
    <div class="tag-cloud compact">
      <span>54 projects</span><span>8 paths</span><span>5 modern labs</span><span>0 logins</span>
    </div>
  </div>
</section>

## Start Here

<div class="start-route-grid">
{start_cards}
</div>

## Current 2026 Home Labs

<div class="project-grid">
{featured_cards}
</div>

## How To Use This Portal

<div class="step-grid">
  <div class="step-card">
    <strong>1. Pick</strong>
    <p>Choose a project by cost, cloud, deployability, and outcome.</p>
  </div>
  <div class="step-card">
    <strong>2. Prepare</strong>
    <p>Use your own credentials and keep secrets out of commits.</p>
  </div>
  <div class="step-card">
    <strong>3. Validate</strong>
    <p>Run the local validation command before provisioning anything.</p>
  </div>
  <div class="step-card">
    <strong>4. Prove</strong>
    <p>Capture outputs, cleanup evidence, and a portfolio-ready summary.</p>
  </div>
</div>

## Keep The Labs Free

<div class="portal-panel">
  <p class="section-kicker">Clean support, no ads</p>
  <h3>Support the portal without interrupting the learning flow.</h3>
  <p>
    The public labs stay open. Paid options support templates, guided review,
    classroom use, and ongoing maintenance without adding ads, popups, or
    account gates to the core guides.
  </p>
  <div class="button-row">
    <a class="portal-button primary" href="{site_path('/support/')}">Support the project</a>
    <a class="portal-button secondary" href="{site_path('/premium-kit/')}">View premium kit</a>
    <a class="portal-button utility" href="{site_path('/for-schools/')}">For schools and teams</a>
  </div>
</div>
"""
    (TARGET_DOCS / "index.mdx").write_text(content, encoding="utf-8")


def start_route_card(route: dict[str, str]) -> str:
    return f"""  <a class="start-route-card" href="{site_path(route['href'])}">
    <span>{escape_html(route['label'])}</span>
    <strong>{escape_html(route['title'])}</strong>
    <p>{escape_html(route['summary'])}</p>
    <small>{escape_html(route['proof'])}</small>
  </a>"""


def hero_route_link(route: dict[str, str]) -> str:
    return f"""      <a href="{site_path(route['href'])}">
        <span>{escape_html(route['label'])}</span>
        <strong>{escape_html(route['title'])}</strong>
      </a>"""


def project_card(project: dict) -> str:
    tool_tags = "".join(
        f'<a href="{tag_href(tool)}">{escape_html(display_tool(tool))}</a>'
        for tool in project["tools"][:6]
    )
    href = project_path(project)
    return f"""  <article class="project-card">
    <a class="project-card-link" href="{href}" aria-label="Open {escape_html(project['name'])}"></a>
    <div class="project-card-body">
      <div class="lab-card-top">
        <span class="status-pill">Project {project['number']:02d}</span>
        <span class="level-pill">{project['skill_level']}</span>
      </div>
      <strong>{escape_html(project['name'])}</strong>
      <p>{escape_html(project['notes'])}</p>
      <dl class="lab-card-facts">
        <div><dt>Time</dt><dd>{project['time_estimate']}</dd></div>
        <div><dt>Cost</dt><dd>{project['cost_risk']}</dd></div>
        <div><dt>Cleanup</dt><dd>{project['cleanup_available']}</dd></div>
        <div><dt>Local</dt><dd>{project['works_locally']}</dd></div>
        <div><dt>Cloud creds</dt><dd>{project['needs_cloud_credentials']}</dd></div>
        <div><dt>Reviewed</dt><dd>{project['last_reviewed']}</dd></div>
      </dl>
      <div class="project-tags" aria-label="Tools used">{tool_tags}</div>
      <p class="proof-line"><span>Proof:</span> {escape_html(project['outcome_proof'])}</p>
    </div>
  </article>"""


def project_path(project: dict) -> str:
    return site_path(f"/projects/{project['route']}/")


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_project_index(projects: list[dict]) -> None:
    cards = "\n".join(project_card(project) for project in projects)
    description = "Browse all 54 DevOps projects without leaving the learning portal."
    content = f"""{frontmatter("Projects", order=1, description=description)}
Every project now has an internal guide page and a standard lab card. Use the
fields to compare level, time, cost, tools, cleanup, credentials, local
support, review date, and portfolio proof before you open a lab. Tool tags are
clickable and open matching project collections.

<div class="project-grid">
{cards}
</div>
"""
    (TARGET_DOCS / "projects" / "index.md").write_text(content, encoding="utf-8")


def write_start_here_page() -> None:
    cards = "\n".join(start_route_card(route) for route in START_ROUTES)
    route_proof_cards = "\n".join(
        f"""  <a class="path-card" href="{site_path(route['href'])}">
    <strong>{escape_html(route['label'])}</strong>
    <p>{escape_html(route['summary'])}</p>
    <small>{escape_html(route['proof'])}</small>
  </a>"""
        for route in START_ROUTES
    )
    content = f"""{frontmatter(
        "Start Here",
        description="Choose the right DevOps learning route before opening a project.",
    )}
Use this page when you do not yet know which project to open. Pick the route
that matches your current goal, then move into the project cards and internal
lab pages.

<div class="start-route-grid">
{cards}
</div>

## Route Proof Checklist

<div class="path-grid">
{route_proof_cards}
</div>

## Before You Run Anything

1. Read the [credentials and cost safety guide]({site_path('/runbooks/credentials-and-cost-safety/')}).
2. Prefer projects marked `Works locally: Yes` while learning a new tool.
3. For cloud labs, confirm `Cleanup: Yes` or write your own destroy checklist before provisioning.
4. Capture validation output and screenshots so the project becomes portfolio evidence, not only practice.
"""
    path = TARGET_DOCS / "catalog" / "start-here.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def project_summary(project: dict) -> str:
    fields = [
        ("Level", project["skill_level"]),
        ("Time", project["time_estimate"]),
        ("Cost", project["cost_risk"]),
        ("Works locally", project["works_locally"]),
        ("Cloud creds", project["needs_cloud_credentials"]),
        ("Cleanup", project["cleanup_available"]),
        ("Reviewed", project["last_reviewed"]),
        ("Validation", f"<code>{escape_html(project['validation'])}</code>"),
    ]
    items = "\n".join(
        f'  <div><span class="meta-label">{label}:</span><strong>{value}</strong></div>'
        for label, value in fields
    )
    return f"""<div class="project-summary">
{items}
</div>"""


def project_tags(project: dict) -> str:
    tags = project["tools"] or ["DevOps"]
    return "".join(
        f'  <a href="{tag_href(tag)}">{escape_html(display_tool(tag))}</a>\n'
        for tag in tags
    )


def tag_catalog(projects: list[dict]) -> list[dict[str, object]]:
    catalog: dict[str, dict[str, object]] = {}
    for project in projects:
        for tool in project["tools"] or ["DevOps"]:
            label = display_tool(tool)
            slug = tag_slug(label)
            entry = catalog.setdefault(
                slug,
                {"slug": slug, "label": label, "count": 0, "projects": []},
            )
            entry["count"] = int(entry["count"]) + 1
            entry["projects"].append(project)
    return sorted(catalog.values(), key=lambda item: (-int(item["count"]), str(item["label"]).lower()))


def tag_card(tag: dict[str, object]) -> str:
    projects = tag["projects"][:4]
    examples = "".join(
        f"<span>#{project['number']:02d}</span>" for project in projects
    )
    href = site_path(f"/tags/{tag['slug']}/")
    return f"""  <a class="tag-card" href="{href}">
    <strong>{escape_html(str(tag['label']))}</strong>
    <p>{int(tag['count'])} project{'s' if int(tag['count']) != 1 else ''}</p>
    <div class="tag-card-examples">{examples}</div>
  </a>"""


def write_tag_pages(projects: list[dict]) -> None:
    tag_dir = TARGET_DOCS / "tags"
    tag_dir.mkdir(parents=True, exist_ok=True)
    catalog = tag_catalog(projects)
    tag_cards = "\n".join(tag_card(tag) for tag in catalog)
    content = f"""{frontmatter("Tags", description="Browse DevOps projects by tool and topic tag.")}
Tags are clickable everywhere in the portal. Use this index when you want to jump
from a tool name to every project that uses it.

<div class="tag-grid">
{tag_cards}
</div>
    """
    (tag_dir / "index.md").write_text(content, encoding="utf-8")

    for tag in catalog:
        related_projects = tag["projects"]
        related_cards = "\n".join(project_card(project) for project in related_projects)
        related_titles = ", ".join(project["name"] for project in related_projects[:8])
        page = f"""{frontmatter(
            str(tag["label"]),
            description=f"Projects that use {tag['label']}.",
        )}
## {escape_html(str(tag['label']))}

<div class="portal-panel">
  <p class="section-kicker">Tag archive</p>
  <h3>{int(tag['count'])} matching project{'s' if int(tag['count']) != 1 else ''}</h3>
  <p>
    Click the cards below to open the project guide, or use the other tag chips
    inside each card to pivot into related topics.
  </p>
  <div class="button-row">
    <a class="portal-button primary" href="{site_path('/tags/')}">Back to all tags</a>
    <a class="portal-button utility" href="{site_path('/projects/')}">Browse all projects</a>
  </div>
</div>

## Matching Projects

{related_cards}

## Sample Matches

{related_titles}
"""
        (tag_dir / f"{tag['slug']}.md").write_text(page, encoding="utf-8")


def architecture_nodes(project: dict) -> list[str]:
    if project["ci_cd"]:
        middle = "CI/CD pipeline"
    elif project["iac"]:
        middle = "IaC plan"
    elif any(tool.lower() == "docker" for tool in project["tools"]):
        middle = "Container build"
    else:
        middle = "Lab steps"

    if project["cloud"]:
        runtime = "/".join(item.upper() for item in project["cloud"]) + " account"
    elif project["deployability"] == "kubernetes_ready":
        runtime = "Local Kubernetes"
    elif project["deployability"] == "container_ready":
        runtime = "Local containers"
    elif project["deployability"] == "local_only":
        runtime = "Local workstation"
    else:
        runtime = "Reference architecture"
    return [
        "Student workstation",
        "Repository files",
        middle,
        runtime,
        "Validation proof",
    ]


def architecture_diagram(project: dict) -> str:
    nodes = "\n".join(
        f"  <span>{escape_html(node)}</span>" for node in architecture_nodes(project)
    )
    return f"""<div class="architecture-flow" aria-label="Architecture diagram">
{nodes}
</div>"""


def prerequisite_items(project: dict) -> str:
    tools = ", ".join(project["tools"][:8]) or "the tools named in the project README"
    credential_text = (
        "Use your own cloud account credentials and keep them out of commits."
        if project["needs_cloud_credentials"] == "Yes"
        else "No cloud provider credentials are required by the project metadata."
    )
    local_text = (
        "This project can be practiced locally before you publish portfolio evidence."
        if project["works_locally"] == "Yes"
        else "This project expects cloud resources, so verify budget alerts and cleanup first."
    )
    return f"""<ul class="lab-checklist">
  <li>Install or review: {escape_html(tools)}.</li>
  <li>{credential_text}</li>
  <li>{local_text}</li>
  <li>Open the safety guide before running commands that create infrastructure.</li>
</ul>"""


def cost_warning(project: dict) -> str:
    cloud = ", ".join(item.upper() for item in project["cloud"]) or "no cloud provider"
    return f"""<div class="lab-warning">
  <strong>Cost and credential stance</strong>
  <p>
    Cost risk is <strong>{project['cost_risk']}</strong>. Cloud target:
    <strong>{escape_html(cloud)}</strong>. Cloud credentials needed:
    <strong>{project['needs_cloud_credentials']}</strong>. Always use your own
    account, never commit secrets, and confirm cleanup before creating paid
    infrastructure.
  </p>
</div>"""


def troubleshooting(project: dict) -> str:
    items = [
        f"Run `{project['validation']}` first so local tooling issues are visible early.",
        "If a command fails, check tool versions, working directory, and required environment variables.",
    ]
    if project["needs_cloud_credentials"] == "Yes":
        items.append(
            "For cloud failures, confirm account identity, region, quotas, and least-privilege IAM."
        )
    if project["ci_cd"]:
        items.append(
            "For pipeline failures, check repository secrets, runner permissions, and pinned action versions."
        )
    if project["deployability"] == "kubernetes_ready":
        items.append(
            "For Kubernetes failures, check the current context, namespace, pod events, and service endpoints."
        )
    return "\n".join(f"- {item}" for item in items)


def cleanup_guidance(project: dict) -> str:
    if project["cleanup_available"] == "Yes":
        return (
            "Cleanup is available or expected for this lab. Use the cleanup or "
            "destroy steps in the guide below, then confirm that local clusters, "
            "containers, cloud resources, buckets, state files, and CI secrets are "
            "no longer active."
        )
    return (
        "No dedicated cleanup command was detected in the project README. Treat "
        "this as a warning: before provisioning anything, write down the exact "
        "delete, destroy, or rollback steps for your environment."
    )


def portfolio_proof(project: dict) -> str:
    return f"""- Validation command output: `{project['validation']}`
- Screenshot or terminal proof: {project['outcome_proof']}
- Notes explaining what changed, what failed, and how you fixed it
- Cleanup evidence, especially for cloud or Kubernetes resources"""


def source_section(project: dict) -> str:
    return f"""<div class="source-callout">
  <strong>Use the guide first.</strong>
  <p>
    The full learning flow stays on this page. Open GitHub only when a step
    asks you to inspect code, fork the lab, or download source assets.
  </p>
  <div class="button-row">
    <a class="portal-button primary" href="{site_path('/runbooks/credentials-and-cost-safety/')}">
      Read safety guide
    </a>
    <a class="portal-button utility" href="{GITHUB_TREE}/{project['dir']}" target="_blank" rel="noopener noreferrer">
      Open project source
    </a>
  </div>
</div>"""


def write_project_pages(projects: list[dict]) -> None:
    project_dir = TARGET_DOCS / "projects"
    project_dir.mkdir(parents=True, exist_ok=True)
    for project in projects:
        raw_readme = project["readme"].read_text(encoding="utf-8")
        source_anchor = original_readme_anchor(raw_readme)
        readme = raw_readme
        readme = strip_first_h1(readme)
        readme = rewrite_project_readme_links(readme, project["dir"])
        readme = demote_markdown_headings(readme)
        tags = project_tags(project)
        summary = project_summary(project)
        content = (
            frontmatter(
                project["name"],
                order=project["number"],
                description=project["notes"],
            )
            + summary
            + f"""\n<div class="project-tags">
{tags}</div>

## Overview

{project['notes']}

## What You Will Build

<div class="lab-detail-grid">
  <div class="lab-panel">
    <span class="meta-label">Outcome</span>
    <strong>{escape_html(project['outcome_proof'])}</strong>
  </div>
  <div class="lab-panel">
    <span class="meta-label">Tools used</span>
    <strong>{escape_html(', '.join(project['tools']) or 'DevOps fundamentals')}</strong>
  </div>
  <div class="lab-panel">
    <span class="meta-label">Best fit</span>
    <strong>{project['skill_level']} - {project['time_estimate']}</strong>
  </div>
</div>

## Architecture Diagram

{architecture_diagram(project)}

## Prerequisites

{prerequisite_items(project)}

## Credentials And Cost Warning

{cost_warning(project)}

## Step-By-Step Lab

Use this flow before you run commands:

1. Read the cost and credential warning above.
2. Review the validation, troubleshooting, cleanup, and portfolio proof sections below.
3. Follow the original project guide preserved near the bottom of this page.
4. Return to the validation and cleanup checks before you capture portfolio evidence.

## Validation Checks

Run the project validation command before and after meaningful changes:

```bash
{project['validation']}
```

## Troubleshooting

{troubleshooting(project)}

## Cleanup

{cleanup_guidance(project)}

## Portfolio Proof

{portfolio_proof(project)}

## Original Project Guide

The original README content is preserved here for lab-specific commands and
context. Headings are intentionally demoted so the page outline stays focused
on the standard lab flow.

"""
            + source_anchor
            + readme
            + f"""

## Source Files On GitHub

{source_section(project)}
"""
        )
        (project_dir / f"{project['route']}.md").write_text(content, encoding="utf-8")


def copy_existing_docs(project_link_map: dict[str, str]) -> None:
    for source in SOURCE_DOCS.rglob("*.md"):
        if "stylesheets" in source.parts:
            continue
        relative = source.relative_to(SOURCE_DOCS)
        if relative.as_posix() == "index.md":
            continue
        target = TARGET_DOCS / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        body = strip_frontmatter(source.read_text(encoding="utf-8"))
        title = page_title(source, body)
        body = strip_first_h1(body)
        body = rewrite_site_links(body, project_link_map, relative)
        target.write_text(frontmatter(title) + body, encoding="utf-8")


def write_catalog_overrides(projects: list[dict]) -> None:
    by_cost = {
        "low": [project for project in projects if project["cost_risk"] == "low"],
        "medium": [project for project in projects if project["cost_risk"] == "medium"],
        "high": [project for project in projects if project["cost_risk"] == "high"],
    }
    row_lines = []
    for project in projects:
        row_lines.append(
            f"| {project['number']:02d} | "
            f"[{project['name']}]({project_path(project)}) | "
            f"{project['skill_level']} | {project['time_estimate']} | "
            f"{project['cost_risk']} | {project['works_locally']} | "
            f"{project['needs_cloud_credentials']} | {project['cleanup_available']} | "
            f"{', '.join(project['tools'][:4])} |"
        )
    rows = "\n".join(row_lines)
    goal_cards = "\n".join(
        f"""  <a class="path-card" href="{site_path(route['href'])}">
    <strong>{escape_html(route['label'])}</strong>
    <p>{escape_html(route['summary'])}</p>
    <small>{escape_html(route['proof'])}</small>
  </a>"""
        for route in START_ROUTES
    )
    quick = "\n".join(
        f"- **{cost.title()} cost:** "
        + ", ".join(
            f"[{project['number']:02d}]({project_path(project)})"
            for project in items[:12]
        )
        for cost, items in by_cost.items()
        if items
    )
    picker_description = (
        "Choose DevOps projects by cost, deployability, and stack "
        "without leaving the portal."
    )
    content = f"""{frontmatter("Project Picker", description=picker_description)}
Use this picker when you know your constraint. Every project link opens an internal guide page.

## Start By Goal

<div class="path-grid">
{goal_cards}
</div>

## Fast Picks

{quick}

## All Projects

| # | Project | Level | Time | Cost | Local | Cloud Credentials | Cleanup | Tools |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{rows}
"""
    path = TARGET_DOCS / "catalog" / "project-picker.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def reset_target() -> None:
    if TARGET_DOCS.exists():
        shutil.rmtree(TARGET_DOCS)
    TARGET_DOCS.mkdir(parents=True, exist_ok=True)


def main() -> None:
    projects = load_projects()
    project_link_map, _ = project_maps(projects)
    reset_target()
    copy_existing_docs(project_link_map)
    write_homepage(projects)
    write_start_here_page()
    write_project_pages(projects)
    write_tag_pages(projects)
    write_project_index(projects)
    write_catalog_overrides(projects)


if __name__ == "__main__":
    main()
