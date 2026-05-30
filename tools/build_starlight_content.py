"""Generate Astro Starlight content from the repository docs and projects."""

from __future__ import annotations

import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DOCS = REPO_ROOT / "docs"
TARGET_DOCS = REPO_ROOT / "src" / "content" / "docs"
SITE_BASE = "/DevOps-Projects"
GITHUB_REPO = "https://github.com/DevCloudNinjas/DevOps-Projects"
GITHUB_TREE = f"{GITHUB_REPO}/tree/master"
GITHUB_BLOB = f"{GITHUB_REPO}/blob/master"
GITHUB_RAW = "https://raw.githubusercontent.com/DevCloudNinjas/DevOps-Projects/master"


def load_projects() -> list[dict]:
    projects: list[dict] = []
    for metadata_path in sorted(REPO_ROOT.glob("project-*/project.yaml")):
        project_dir = metadata_path.parent
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        project = metadata["project"]
        number = int(project["number"])
        slug = project["slug"]
        route = f"{number:02d}-{slug}"
        projects.append(
            {
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
                "readme": project_dir / "README.md",
            }
        )
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
            return f"![{alt}]({target}{title})"
        source_path, _ = repo_source_path(project_dir, target)
        raw_path = quote(source_path, safe="/:@")
        return f"![{alt}]({GITHUB_RAW}/{raw_path}{title})"

    def replace_link(match: re.Match[str]) -> str:
        label, raw_target = match.group(1), match.group(2)
        target, title = split_markdown_destination(raw_target)
        if is_external_or_anchor(target):
            return match.group(0)
        source_path, fragment = repo_source_path(project_dir, target)
        if source_path.lower() in {f"{project_dir}/readme.md", "readme.md", ""}:
            anchor = f"#{fragment}" if fragment else "#_top"
            return f"[{label}]({anchor})"
        blob_path = quote(source_path, safe="/:@")
        if fragment:
            blob_path += f"#{fragment}"
        return f"[{label}]({GITHUB_BLOB}/{blob_path}{title})"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, text)
    text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
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


def strip_first_h1(text: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", text, count=1, flags=re.MULTILINE).lstrip()


def write_homepage(projects: list[dict]) -> None:
    featured_numbers = {50, 51, 52, 53, 54}
    featured = [
        project for project in projects if project["number"] in featured_numbers
    ]
    featured_cards = "\n".join(project_card(project) for project in featured)
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
      <a class="portal-button primary" href="{site_path('/projects/')}">Browse projects</a>
      <a class="portal-button secondary" href="{site_path('/learning-paths/')}">Choose a path</a>
      <a class="portal-button" href="{site_path('/runbooks/credentials-and-cost-safety/')}">Read the safety guide</a>
    </div>
  </div>
  <div class="hero-metrics" aria-label="Repository snapshot">
    <div class="metric-grid">
      <div class="metric"><strong>54</strong><span>internal project guides</span></div>
      <div class="metric"><strong>8</strong><span>learning paths</span></div>
      <div class="metric"><strong>5</strong><span>modern home labs</span></div>
      <div class="metric"><strong>0</strong><span>required logins</span></div>
    </div>
    <div class="tag-cloud">
      <span>AWS</span><span>Azure</span><span>Docker</span><span>Kubernetes</span>
      <span>Terraform</span><span>OpenTofu</span><span>Jenkins</span>
      <span>GitHub Actions</span><span>Argo CD</span><span>Trivy</span>
      <span>OpenTelemetry</span><span>Cosign</span>
    </div>
  </div>
</section>

## Start With The Right Project

<div class="path-grid">
  <a class="path-card" href="{site_path('/learning-paths/beginner/')}">
    <strong>Beginner track</strong>
    <p>Linux, first delivery, simple CI/CD, and one local GitOps lab.</p>
  </a>
  <a class="path-card" href="{site_path('/learning-paths/docker-kubernetes/')}">
    <strong>Containers and clusters</strong>
    <p>Docker packaging, Kubernetes manifests, GitOps, and canary delivery.</p>
  </a>
  <a class="path-card" href="{site_path('/learning-paths/terraform-iac/')}">
    <strong>Infrastructure as code</strong>
    <p>Terraform, OpenTofu, VPCs, EKS, ECS, serverless, and cleanup habits.</p>
  </a>
  <a class="path-card" href="{site_path('/learning-paths/devsecops/')}">
    <strong>DevSecOps</strong>
    <p>Trivy, SBOMs, signing, secrets hygiene, and secure pipeline design.</p>
  </a>
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
"""
    (TARGET_DOCS / "index.mdx").write_text(content, encoding="utf-8")


def project_card(project: dict) -> str:
    stack = ", ".join(project["stack"][:4])
    href = project_path(project)
    return f"""  <a class="project-card" href="{href}">
    <span class="status-pill">Project {project['number']:02d}</span>
    <strong>{escape_html(project['name'])}</strong>
    <p>{escape_html(project['notes'])}</p>
    <div class="project-tags">
      <span>{project['cost_risk']} cost</span>
      <span>{project['deployability'].replace('_', ' ')}</span>
      <span>{escape_html(stack)}</span>
    </div>
  </a>"""


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
Every project now has an internal guide page. Use GitHub only when you need
to inspect source files or fork the repository.

<div class="project-grid">
{cards}
</div>
"""
    (TARGET_DOCS / "projects" / "index.md").write_text(content, encoding="utf-8")


def write_project_pages(projects: list[dict]) -> None:
    project_dir = TARGET_DOCS / "projects"
    project_dir.mkdir(parents=True, exist_ok=True)
    for project in projects:
        readme = project["readme"].read_text(encoding="utf-8")
        readme = strip_first_h1(readme)
        readme = rewrite_project_readme_links(readme, project["dir"])
        tags = "".join(
            f"  <span>{escape_html(tag)}</span>\n"
            for tag in project["stack"]
            + project["cloud"]
            + project["iac"]
            + project["ci_cd"]
        )
        summary = f"""<div class="project-summary">
  <div><span class="meta-label">Cost</span><strong>{project['cost_risk']}</strong></div>
  <div>
    <span class="meta-label">Deployability</span>
    <strong>{project['deployability'].replace('_', ' ')}</strong>
  </div>
  <div>
    <span class="meta-label">Status</span>
    <strong>{project['status'].replace('_', ' ')}</strong>
  </div>
  <div>
    <span class="meta-label">Validation</span>
    <strong><code>{escape_html(project['validation'])}</code></strong>
  </div>
</div>

<div class="project-tags">
{tags}</div>

<div class="source-callout">
  <strong>Use the guide first.</strong>
  <p>
    The full learning guide is on this page. Open the repository files only
    when a step asks you to inspect code, fork the project, or download raw
    assets.
  </p>
  <div class="button-row">
    <a class="portal-button primary" href="{site_path('/runbooks/credentials-and-cost-safety/')}">
      Read safety guide
    </a>
    <a class="portal-button utility" href="{GITHUB_TREE}/{project['dir']}">Project files on GitHub</a>
  </div>
</div>
"""
        content = (
            frontmatter(
                project["name"],
                order=project["number"],
                description=project["notes"],
            )
            + summary
            + "\n## Project Guide\n\n"
            + readme
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
            f"{project['deployability'].replace('_', ' ')} | "
            f"{project['cost_risk']} | {', '.join(project['stack'][:4])} |"
        )
    rows = "\n".join(row_lines)
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

## Fast Picks

{quick}

## All Projects

| # | Project | Deployability | Cost Risk | Stack |
| --- | --- | --- | --- | --- |
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
    write_project_pages(projects)
    write_project_index(projects)
    write_catalog_overrides(projects)


if __name__ == "__main__":
    main()
