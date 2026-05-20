"""Project inventory helpers for root-level validation commands."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from tools.quality_gate import QualityGate, _print_report


DEFAULT_METADATA_PATH = Path("tools/project_metadata.json")

LEARNING_PATHS = (
    "cloud-foundations",
    "containers",
    "ci-cd",
    "infrastructure-as-code",
    "kubernetes",
    "devsecops",
    "observability",
    "serverless",
    "platform-engineering",
    "security",
)

LEARNER_BADGES = (
    "beginner-friendly",
    "local-first",
    "free-tier-aware",
    "cloud-cost-risk",
    "portfolio-ready",
    "team-workflow",
    "security-focused",
    "needs-cloud-account",
    "cleanup-required",
    "capstone",
)


@dataclass(frozen=True)
class Project:
    """A project discovered from repository metadata."""

    id: str
    path: str
    name: str
    source: str


def load_metadata(repo_root: Path, metadata_path: Path | str | None = None) -> dict:
    """Load project metadata from the repo."""

    path = Path(metadata_path) if metadata_path else DEFAULT_METADATA_PATH
    full_path = path if path.is_absolute() else repo_root / path
    return json.loads(full_path.read_text(encoding="utf-8"))


def discover_projects(repo_root: Path, metadata: dict | None = None) -> list[Project]:
    """Discover projects from metadata globs."""

    metadata = metadata or load_metadata(repo_root)
    projects: dict[str, Project] = {}
    for root in metadata.get("project_roots", []):
        pattern = root["glob"]
        source = root.get("name", pattern)
        for match in repo_root.glob(pattern):
            if not match.is_dir():
                continue
            relative_path = match.relative_to(repo_root).as_posix()
            project_id = relative_path.replace("/", "__")
            projects[relative_path] = Project(
                id=project_id,
                path=relative_path,
                name=match.name,
                source=source,
            )
    return sorted(projects.values(), key=lambda project: project.path)


def validate_metadata(repo_root: Path, metadata: dict | None = None) -> list[str]:
    """Return metadata validation errors."""

    metadata = metadata or load_metadata(repo_root)
    errors: list[str] = []
    roots = metadata.get("project_roots")
    if not isinstance(roots, list) or not roots:
        errors.append("metadata must define a non-empty project_roots list")
        return errors

    for index, root in enumerate(roots):
        if not isinstance(root, dict):
            errors.append(f"project_roots[{index}] must be an object")
            continue
        pattern = root.get("glob")
        if not isinstance(pattern, str) or not pattern:
            errors.append(f"project_roots[{index}].glob must be a non-empty string")
            continue
        if Path(pattern).is_absolute() or ".." in Path(pattern).parts:
            errors.append(f"project_roots[{index}].glob must stay inside the repository")

    conventions = metadata.get("learner_metadata", {})
    if conventions:
        if not isinstance(conventions, dict):
            errors.append("learner_metadata must be an object when provided")
        else:
            paths = conventions.get("learning_paths", [])
            badges = conventions.get("badges", [])
            if not isinstance(paths, list) or set(paths) - set(LEARNING_PATHS):
                errors.append("learner_metadata.learning_paths must use the supported learning path tags")
            if not isinstance(badges, list) or set(badges) - set(LEARNER_BADGES):
                errors.append("learner_metadata.badges must use the supported learner badge tags")

    if not discover_projects(repo_root, metadata):
        errors.append("metadata did not discover any projects")
    return errors


def changed_files(repo_root: Path, base_ref: str, head_ref: str = "HEAD") -> list[str]:
    """Return changed file paths between two git refs."""

    ranges = [f"{base_ref}...{head_ref}", f"{base_ref}..{head_ref}"]
    last_error = ""
    for diff_range in ranges:
        result = subprocess.run(
            ["git", "diff", "--name-only", diff_range],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return [line for line in result.stdout.splitlines() if line]
        last_error = result.stderr.strip()
    raise RuntimeError(f"could not compute changed files: {last_error}")


def projects_for_changed_files(projects: Iterable[Project], paths: Iterable[str]) -> list[Project]:
    """Return projects that contain at least one changed path."""

    by_path = {project.path: project for project in projects}
    selected: dict[str, Project] = {}
    for changed_path in paths:
        for project_path, project in by_path.items():
            if changed_path == project_path or changed_path.startswith(f"{project_path}/"):
                selected[project_path] = project
    return sorted(selected.values(), key=lambda project: project.path)


def validate_project(repo_root: Path, project: str) -> int:
    """Run the repository quality gate for one project."""

    projects = {item.path: item for item in discover_projects(repo_root)}
    if project not in projects:
        print(f"Unknown project: {project}")
        print("Run `make list-projects` to see valid project paths.")
        return 2

    findings = QualityGate(repo_root, project_path=project).run()
    _print_report(findings)
    return 1 if findings else 0


def _format_projects(projects: list[Project], output_format: str) -> str:
    if output_format == "json":
        return json.dumps([asdict(project) for project in projects], indent=2)
    if output_format == "github-matrix":
        return json.dumps({"include": [asdict(project) for project in projects]}, separators=(",", ":"))
    return "\n".join(project.path for project in projects)


def build_list_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List projects discovered from repository metadata.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--metadata", default=None, help="Metadata JSON path. Defaults to tools/project_metadata.json.")
    parser.add_argument(
        "--format",
        choices=("plain", "json", "github-matrix"),
        default="plain",
        help="Output format.",
    )
    parser.add_argument("--changed-from", default=None, help="Git base ref for changed-project detection.")
    parser.add_argument("--changed-to", default="HEAD", help="Git head ref for changed-project detection.")
    parser.add_argument("--validate-metadata", action="store_true", help="Validate metadata before listing.")
    return parser


def list_main(argv: list[str] | None = None) -> int:
    args = build_list_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    metadata = load_metadata(repo_root, args.metadata)
    errors = validate_metadata(repo_root, metadata) if args.validate_metadata else []
    if errors:
        for error in errors:
            print(f"metadata error: {error}", file=sys.stderr)
        return 1

    projects = discover_projects(repo_root, metadata)
    if args.changed_from:
        projects = projects_for_changed_files(
            projects,
            changed_files(repo_root, args.changed_from, args.changed_to),
        )
    print(_format_projects(projects, args.format))
    return 0


def build_validate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate one project with the local quality gate.")
    parser.add_argument("project", help="Project path, for example project-31-cloud-native-monitoring.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    return parser


def validate_main(argv: list[str] | None = None) -> int:
    args = build_validate_parser().parse_args(argv)
    return validate_project(Path(args.repo_root).resolve(), args.project)
