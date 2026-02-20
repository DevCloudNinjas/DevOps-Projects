"""File discovery and scanning for the repo consolidation pipeline.

Provides recursive file walking with binary detection, symlink loop
handling, encoding fallback, and permission error resilience.
"""

from __future__ import annotations

import logging
import os
import re
from collections.abc import Iterator
from pathlib import Path

from tools.repo_consolidation.models import Finding

logger = logging.getLogger(__name__)

# Directories to skip during traversal.
SKIP_DIRS: frozenset[str] = frozenset({
    ".git",
    "node_modules",
    ".terraform",
    "__pycache__",
})

# Number of bytes to read for binary detection.
_BINARY_CHECK_SIZE = 8192


def is_binary(file_path: Path) -> bool:
    """Return ``True`` if *file_path* appears to be a binary file.

    Reads the first 8 KB and checks for null bytes.  Files that cannot
    be read (permission errors, etc.) are treated as binary so they are
    skipped rather than crashing the pipeline.
    """
    try:
        with open(file_path, "rb") as fh:
            chunk = fh.read(_BINARY_CHECK_SIZE)
        return b"\x00" in chunk
    except OSError as exc:
        logger.warning("Cannot read file for binary check, skipping: %s (%s)", file_path, exc)
        return True


def read_text(file_path: Path) -> str | None:
    """Read *file_path* as text with encoding fallback.

    Tries UTF-8 first, then falls back to latin-1.  Returns ``None``
    if the file cannot be read at all (permission error, etc.).
    """
    for encoding in ("utf-8", "latin-1"):
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            logger.warning("Permission/OS error reading %s: %s", file_path, exc)
            return None
    # Should not happen — latin-1 accepts all byte values — but guard anyway.
    logger.warning("Could not decode file with any encoding: %s", file_path)
    return None


def discover_files(repo_root: str | Path) -> Iterator[Path]:
    """Yield paths to every text file under *repo_root*.

    Walks the directory tree recursively, skipping:
    * directories listed in :data:`SKIP_DIRS`
    * binary files (detected via null-byte check)
    * symlink loops (tracked by real path)

    Permission errors on directories or files are logged and skipped.
    """
    root = Path(repo_root).resolve()
    visited_real_dirs: set[str] = set()

    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        current = Path(dirpath)

        # --- symlink loop detection ---
        try:
            real_dir = str(current.resolve(strict=True))
        except OSError as exc:
            logger.warning("Cannot resolve directory, skipping: %s (%s)", current, exc)
            dirnames.clear()
            continue

        if real_dir in visited_real_dirs:
            logger.debug("Symlink loop detected, skipping: %s -> %s", current, real_dir)
            dirnames.clear()
            continue
        visited_real_dirs.add(real_dir)

        # --- prune skipped directories (in-place so os.walk respects it) ---
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS
        ]

        # --- yield text files ---
        for fname in filenames:
            fpath = current / fname
            if not fpath.is_file():
                continue
            if is_binary(fpath):
                logger.debug("Skipping binary file: %s", fpath)
                continue
            yield fpath


# ---------------------------------------------------------------------------
# Scan patterns — keyed by issue type
# ---------------------------------------------------------------------------

#: Old standalone repo URLs with case-insensitive org name.
_OLD_URL_PATTERN = re.compile(
    r"github\.com/(DevCloudNinjas|devcloudninjas)/([^/\s\)\"']+)",
    re.IGNORECASE,
)

#: GitHub Personal Access Tokens.
_PAT_PATTERN = re.compile(r"ghp_[A-Za-z0-9_]{36}")

#: AWS ECR registry URLs with 12-digit account IDs.
_ECR_PATTERN = re.compile(
    r"\d{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com"
)

#: Hardcoded Docker image references using the old org name.
_DOCKER_IMAGE_PATTERN = re.compile(
    r'docker\.build\(["\']devcloudninjas["\']',
    re.IGNORECASE,
)

#: Generic hardcoded ``devcloudninjas`` image name references (e.g. in
#: YAML image fields or Jenkinsfile string literals) that are *not*
#: already captured by the URL or docker.build patterns.
#:
#: This pattern is intentionally simple — context filtering is done in
#: :func:`_is_docker_image_context` to avoid false positives in prose,
#: Go code, cspell dictionaries, filenames, etc.
_DOCKER_IMAGE_NAME_PATTERN = re.compile(
    r"(?<![/\w@])devcloudninjas(?![/\w@'.])",
    re.IGNORECASE,
)

#: Patterns that indicate a line is in a Docker image context.
_DOCKER_CONTEXT_INDICATORS = re.compile(
    r"(?:"
    r"^\s*image\s*[:=]"          # YAML image: or assignment
    r"|docker\s+(?:push|pull|tag|run|build)"  # docker CLI commands
    r"|docker\.(?:build|push|pull)"           # Jenkinsfile docker methods
    r"|FROM\s+"                               # Dockerfile FROM
    r"|\.dkr\.ecr\."                          # ECR URL on same line
    r"|dockerImage\s*="                       # variable assignment
    r"|DOCKER_IMAGE"                          # env var name
    r"|container_name\s*:"                    # docker-compose
    r")",
    re.IGNORECASE,
)


def _is_docker_image_context(line: str, file_type: str) -> bool:
    """Return True if *line* is in a context where ``devcloudninjas`` is a Docker image name.

    Only matches in Dockerfiles, Jenkinsfiles, YAML image fields, and
    lines containing ECR URLs or docker commands.  Shell scripts are
    only flagged when the line itself contains a docker command.
    """
    # Jenkinsfiles and Dockerfiles are always Docker-relevant
    if file_type in ("Jenkinsfile", "Dockerfile"):
        return True
    # Check for Docker-specific line patterns (works for all file types
    # including shell scripts, YAML, etc.)
    if _DOCKER_CONTEXT_INDICATORS.search(line):
        return True
    return False

#: Private key file extensions.
_PRIVATE_KEY_FILE_PATTERN = re.compile(r"\.(ppk|pem)$", re.IGNORECASE)

#: Convenience mapping of issue type → compiled regex used for
#: *line-by-line* content scanning.
SCAN_PATTERNS: dict[str, re.Pattern[str]] = {
    "old_url": _OLD_URL_PATTERN,
    "credential": _PAT_PATTERN,
    "hardcoded_account_id": _ECR_PATTERN,
    "stale_docker_image": _DOCKER_IMAGE_PATTERN,
}

# The consolidated repo name — matches against this are *not* old URLs.
_CONSOLIDATED_REPO_NAME = "DevOps-Projects"

# Repo names that are subfolders of the consolidated repo itself — skip these.
_SELF_REFERENCE_PATTERN = re.compile(
    r"^project-\d+",
    re.IGNORECASE,
)

# Pattern to detect hash-like strings (not repo names).
_HASH_PATTERN = re.compile(r"^[0-9a-f]{20,}$")


def _file_type(file_path: Path) -> str:
    """Return a normalised file-type string for *file_path*.

    Special filenames (``Jenkinsfile``, ``Dockerfile``, …) are returned
    as-is.  Everything else returns the lowercase extension including the
    leading dot (e.g. ``.md``).
    """
    name = file_path.name
    if name in {"Jenkinsfile", "Dockerfile", "Makefile", "Vagrantfile"}:
        return name
    ext = file_path.suffix.lower()
    return ext if ext else name


def _extract_repo_name(match: re.Match[str]) -> str:
    """Extract the old repo name from an ``_OLD_URL_PATTERN`` match.

    Strips trailing ``/``, URL fragments, markdown/HTML artifacts,
    and ``.git`` suffix.
    """
    name = match.group(2).rstrip("/")
    # Strip trailing URL fragments and markdown/HTML artifacts first
    name = name.split("#")[0].split("?")[0]
    name = name.rstrip("`<>),;:!.")
    # Strip .git suffix after cleaning artifacts
    if name.endswith(".git"):
        name = name[:-4]
    return name


def scan_repo(
    repo_root: str | Path,
    patterns: dict[str, re.Pattern[str]] | None = None,
) -> list[Finding]:
    """Scan every text file under *repo_root* and return all findings.

    Parameters
    ----------
    repo_root:
        Path to the repository root directory.
    patterns:
        Optional mapping of ``issue_type → compiled regex``.  Defaults
        to :data:`SCAN_PATTERNS` when *None*.

    Returns
    -------
    list[Finding]
        One :class:`Finding` per match, with ``file_path`` relative to
        *repo_root*.
    """
    if patterns is None:
        patterns = SCAN_PATTERNS

    root = Path(repo_root).resolve()
    findings: list[Finding] = []

    for fpath in discover_files(repo_root):
        rel_path = str(fpath.relative_to(root))
        ft = _file_type(fpath)

        # --- private key file detection (filename-based) ---
        if _PRIVATE_KEY_FILE_PATTERN.search(fpath.name):
            findings.append(
                Finding(
                    file_path=rel_path,
                    line_number=0,
                    matched_text=fpath.name,
                    issue_type="credential",
                    old_repo_name="",
                    context=f"Private key file: {fpath.name}",
                    file_type=ft,
                )
            )

        # --- line-by-line content scanning ---
        content = read_text(fpath)
        if content is None:
            continue

        for line_no, line in enumerate(content.splitlines(), start=1):
            for issue_type, pattern in patterns.items():
                for m in pattern.finditer(line):
                    matched = m.group(0)

                    # For old_url: skip references to the consolidated repo itself,
                    # self-references to project subfolders, and hash-like strings.
                    if issue_type == "old_url":
                        repo_name = _extract_repo_name(m)
                        if repo_name == _CONSOLIDATED_REPO_NAME:
                            continue
                        if _SELF_REFERENCE_PATTERN.match(repo_name):
                            continue
                        if _HASH_PATTERN.match(repo_name):
                            continue
                        if not repo_name:
                            continue
                    else:
                        repo_name = ""

                    findings.append(
                        Finding(
                            file_path=rel_path,
                            line_number=line_no,
                            matched_text=matched,
                            issue_type=issue_type,
                            old_repo_name=repo_name,
                            context=line,
                            file_type=ft,
                        )
                    )

            # --- devcloudninjas image name (not caught by URL/docker.build) ---
            # Only flag if the line does NOT already contain a github.com URL
            # or a docker.build call (those are handled above), AND the line
            # is in a Docker-relevant context.
            if _DOCKER_IMAGE_NAME_PATTERN.search(line):
                if (
                    not _OLD_URL_PATTERN.search(line)
                    and not _DOCKER_IMAGE_PATTERN.search(line)
                    and _is_docker_image_context(line, ft)
                ):
                    for m in _DOCKER_IMAGE_NAME_PATTERN.finditer(line):
                        findings.append(
                            Finding(
                                file_path=rel_path,
                                line_number=line_no,
                                matched_text=m.group(0),
                                issue_type="stale_docker_image",
                                old_repo_name="",
                                context=line,
                                file_type=ft,
                            )
                        )

    return findings
