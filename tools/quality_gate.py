"""Fast, local repository quality gates.

The checks in this module intentionally avoid cloud services and heavyweight
builds. They are meant to catch repository hygiene regressions early while
staying practical for a large learning repository with archived examples.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by users without dev deps.
    yaml = None


YAML_EXTENSIONS = {".yaml", ".yml"}
TEXT_EXTENSIONS = {
    ".cfg",
    ".conf",
    ".env",
    ".ini",
    ".json",
    ".md",
    ".properties",
    ".py",
    ".sh",
    ".tf",
    ".tfvars",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
MAX_SECRET_SCAN_BYTES = 2_000_000

INTENTIONAL_SECRET_FIXTURE_PATTERNS = (
    "tools/repo_consolidation/tests/**",
    "**/fixtures/**",
    "**/fixture/**",
    "**/test/**",
    "**/tests/**",
    "**/easybuggy/**",
    "**/vulnerabilities/**",
    "**/security-fixtures/**",
)

TEMPLATED_YAML_PATTERNS = (
    "**/charts/**/templates/**",
    "**/helm/**/templates/**",
)

KNOWN_NON_SHELL_SCRIPTS = {
    Path("project-47-django-saas-ecommerce/deployments/scripts/django-shell.sh"),
}

SECRET_PATTERNS = (
    (
        "AWS access key id",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
    (
        "AWS secret access key assignment",
        re.compile(
            r"(?i)\b(?:aws_)?secret(?:_access)?_key\b\s*[:=]\s*['\"]?"
            r"[A-Za-z0-9/+=]{32,}",
        ),
    ),
    (
        "GitHub token",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    ),
    (
        "Slack token",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    ),
    (
        "private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "generic secret assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|token|password|passwd|secret)\b"
            r"[ \t]*[:=][ \t]*['\"]?(?P<value>[A-Za-z0-9_./+=${}-]{16,})",
        ),
    ),
)

PLACEHOLDER_VALUE_PARTS = (
    "base64-encoded",
    "example",
    "placeholder",
    "replace",
    "token-generated",
    "your-",
)

REFERENCE_VALUE_PREFIXES = (
    "$",
    "${{",
    "${",
    "/",
    "readonly",
    "data.",
    "local.",
    "module.",
    "os.environ",
    "self.",
    "settings.",
    "var.",
)


@dataclass(frozen=True)
class Finding:
    """A single quality gate failure."""

    check: str
    path: Path
    message: str
    line: int | None = None

    def format(self) -> str:
        location = str(self.path)
        if self.line is not None:
            location = f"{location}:{self.line}"
        return f"[{self.check}] {location} - {self.message}"


class IgnoreUnknownTagsLoader(yaml.SafeLoader if yaml else object):
    """YAML loader that accepts CloudFormation/SAM custom tags."""


if yaml:

    def _unknown_yaml_tag(loader: yaml.Loader, tag_suffix: str, node: yaml.Node):
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node)
        if isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        return loader.construct_scalar(node)

    IgnoreUnknownTagsLoader.add_multi_constructor("!", _unknown_yaml_tag)


def is_intentional_secret_fixture(path: Path) -> bool:
    """Return whether a path is intentionally allowed to contain scanner bait."""

    normalized = path.as_posix()
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in INTENTIONAL_SECRET_FIXTURE_PATTERNS)


def is_templated_yaml(path: Path) -> bool:
    normalized = path.as_posix()
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in TEMPLATED_YAML_PATTERNS)


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _looks_like_placeholder_or_reference(match: re.Match[str]) -> bool:
    value = match.groupdict().get("value")
    if not value:
        return False
    normalized = value.strip("'\"").lower()
    if normalized.startswith(REFERENCE_VALUE_PREFIXES):
        return True
    if set(normalized) <= {"x", "-"}:
        return True
    if normalized.startswith("abcdef."):
        return True
    return any(part in normalized for part in PLACEHOLDER_VALUE_PARTS)


class QualityGate:
    """Run fast repository quality checks."""

    def __init__(self, repo_root: Path | str, project_path: Path | str | None = None) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.project_path = self._normalize_project_path(project_path)

    def _normalize_project_path(self, project_path: Path | str | None) -> Path | None:
        if project_path is None:
            return None
        raw_path = Path(project_path)
        full_path = raw_path if raw_path.is_absolute() else self.repo_root / raw_path
        try:
            relative_path = full_path.resolve().relative_to(self.repo_root)
        except ValueError as exc:
            raise ValueError(f"project path must be inside repo root: {project_path}") from exc
        return relative_path

    def run(self) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(self.check_tracked_ignored_files())
        findings.extend(self.check_secret_patterns())
        findings.extend(self.check_syntax())
        findings.extend(self.check_node_package_locks())
        return findings

    def git_files(self, *patterns: str) -> list[Path]:
        cmd = ["git", "ls-files", *patterns]
        result = subprocess.run(
            cmd,
            cwd=self.repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        paths = [Path(line) for line in result.stdout.splitlines() if line]
        if self.project_path is None:
            return paths
        return [path for path in paths if path == self.project_path or self.project_path in path.parents]

    def check_tracked_ignored_files(self) -> list[Finding]:
        result = subprocess.run(
            ["git", "ls-files", "-ci", "--exclude-standard"],
            cwd=self.repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return [
            Finding(
                check="tracked-ignored",
                path=Path(path),
                message=(
                    "file is tracked by git but now matches .gitignore; "
                    "remove it from the index or adjust .gitignore"
                ),
            )
            for path in result.stdout.splitlines()
            if path
            and (self.project_path is None or Path(path) == self.project_path or self.project_path in Path(path).parents)
            and (self.repo_root / path).exists()
        ]

    def check_secret_patterns(self) -> list[Finding]:
        findings: list[Finding] = []
        for path in self.git_files():
            full_path = self.repo_root / path
            if not full_path.is_file() or is_intentional_secret_fixture(path):
                continue
            if full_path.suffix.lower() not in TEXT_EXTENSIONS and "." in full_path.name:
                continue
            try:
                if full_path.stat().st_size > MAX_SECRET_SCAN_BYTES:
                    continue
                data = full_path.read_bytes()
            except OSError as exc:
                findings.append(Finding("secret-pattern", path, f"could not read file: {exc}"))
                continue
            if b"\0" in data:
                continue
            text = data.decode("utf-8", errors="ignore")
            for label, pattern in SECRET_PATTERNS:
                match = pattern.search(text)
                if match:
                    if label == "generic secret assignment" and _looks_like_placeholder_or_reference(match):
                        continue
                    findings.append(
                        Finding(
                            check="secret-pattern",
                            path=path,
                            line=_line_number(text, match.start()),
                            message=f"possible {label}; replace with a documented placeholder",
                        ),
                    )
                    break
        return findings

    def check_syntax(self) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(self.check_yaml_syntax())
        findings.extend(self.check_shell_syntax())
        findings.extend(self.check_python_syntax())
        return findings

    def check_yaml_syntax(self) -> list[Finding]:
        if yaml is None:
            return [
                Finding(
                    "yaml-syntax",
                    Path("tools/requirements.txt"),
                    "PyYAML is required for YAML validation; run pip install -r tools/requirements.txt",
                ),
            ]
        findings: list[Finding] = []
        for path in self.git_files("*.yaml", "*.yml"):
            full_path = self.repo_root / path
            if not full_path.is_file() or is_templated_yaml(path):
                continue
            try:
                text = full_path.read_text(encoding="utf-8")
                list(yaml.load_all(text, Loader=IgnoreUnknownTagsLoader))
            except Exception as exc:
                findings.append(Finding("yaml-syntax", path, str(exc).splitlines()[0]))
        return findings

    def check_shell_syntax(self) -> list[Finding]:
        findings: list[Finding] = []
        for path in self.git_files("*.sh"):
            full_path = self.repo_root / path
            if not full_path.is_file() or path in KNOWN_NON_SHELL_SCRIPTS:
                continue
            result = subprocess.run(
                ["bash", "-n", str(full_path)],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
            )
            if result.returncode:
                message = (result.stderr or result.stdout).strip().splitlines()[0]
                findings.append(Finding("shell-syntax", path, message))
        return findings

    def check_python_syntax(self) -> list[Finding]:
        findings: list[Finding] = []
        for path in self.git_files("*.py"):
            full_path = self.repo_root / path
            if not full_path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                ast.parse(full_path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                findings.append(
                    Finding(
                        "python-syntax",
                        path,
                        exc.msg,
                        line=exc.lineno,
                    ),
                )
            except UnicodeDecodeError as exc:
                findings.append(Finding("python-syntax", path, f"could not decode as UTF-8: {exc}"))
        return findings

    def check_node_package_locks(self) -> list[Finding]:
        findings: list[Finding] = []
        for path in self.git_files("**/package.json", "package.json"):
            full_path = self.repo_root / path
            if not full_path.is_file():
                continue
            try:
                json.loads(full_path.read_text(encoding="utf-8"))
            except Exception as exc:
                findings.append(Finding("node-package-lock", path, f"invalid package.json: {exc}"))

        for path in self.git_files("**/package-lock.json", "package-lock.json"):
            full_path = self.repo_root / path
            if not full_path.is_file():
                continue
            package_json = full_path.parent / "package.json"
            if not package_json.is_file():
                findings.append(
                    Finding(
                        "node-package-lock",
                        path,
                        "package-lock.json has no package.json in the same directory",
                    ),
                )
                continue
            try:
                data = json.loads(full_path.read_text(encoding="utf-8"))
            except Exception as exc:
                findings.append(Finding("node-package-lock", path, f"invalid package-lock.json: {exc}"))
                continue
            if "lockfileVersion" not in data:
                findings.append(Finding("node-package-lock", path, "missing lockfileVersion"))
            if "packages" not in data and "dependencies" not in data:
                findings.append(Finding("node-package-lock", path, "missing packages/dependencies data"))

        for path in self.git_files("**/yarn.lock", "yarn.lock"):
            full_path = self.repo_root / path
            if not full_path.is_file():
                continue
            text = full_path.read_text(encoding="utf-8", errors="ignore")
            if "<<<<<<<" in text or "=======" in text or ">>>>>>>" in text:
                findings.append(Finding("node-package-lock", path, "lock file contains merge conflict markers"))
            if not text.strip():
                findings.append(Finding("node-package-lock", path, "lock file is empty"))
        return findings


def _print_report(findings: Iterable[Finding]) -> None:
    findings = list(findings)
    if not findings:
        print("Quality gate passed: no failures found.")
        return
    print(f"Quality gate failed: {len(findings)} failure(s) found.")
    for finding in findings:
        print(f"  - {finding.format()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fast local repository quality gates.")
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=".",
        help="Repository root to validate. Defaults to the current directory.",
    )
    parser.add_argument(
        "--project",
        default=None,
        help="Optional project path to validate instead of the whole repository.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        findings = QualityGate(args.repo_root, project_path=args.project).run()
    except ValueError as exc:
        print(f"Quality gate failed: {exc}")
        return 1
    _print_report(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
