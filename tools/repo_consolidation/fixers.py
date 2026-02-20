"""Fixer components for the repo consolidation remediation pipeline.

Each fixer function takes a :class:`Finding` and returns a
:class:`Replacement` describing how to remediate the issue in place.

This module currently contains the old-URL fixer.  Additional fixers
(credentials, account IDs, Docker images) will be added in subsequent
tasks.

Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 4.2, 4.3, 4.5,
              7.2, 8.2, 8.3, 9.1, 9.2
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import PurePosixPath

from tools.repo_consolidation.models import Finding, Replacement
from tools.repo_consolidation import url_map as umap

logger = logging.getLogger(__name__)

# Regex to detect the old GitHub URL pattern (mirrors scanner pattern).
_OLD_URL_RE = re.compile(
    r"https?://github\.com/(DevCloudNinjas|devcloudninjas)/([^/\s\)\"']+)",
    re.IGNORECASE,
)

# Regex for markdown link syntax: [text](url)
_MARKDOWN_LINK_RE = re.compile(
    r"\[([^\]]*)\]\((https?://github\.com/(DevCloudNinjas|devcloudninjas)/[^)]+)\)",
    re.IGNORECASE,
)

# Regex for git clone commands
_GIT_CLONE_RE = re.compile(r"git\s+clone\s+", re.IGNORECASE)

# Regex for Go import paths (no https:// prefix)
_GO_IMPORT_RE = re.compile(
    r'github\.com/(DevCloudNinjas|devcloudninjas)/([^/\s"\']+)(/[^"\s\']*)?',
    re.IGNORECASE,
)


def _extract_subpath(old_url: str, old_repo_name: str) -> str:
    """Extract the subpath after the repo name from *old_url*.

    For example, given
    ``https://github.com/DevCloudNinjas/Zomato-Clone/blob/main/docs/setup.md``
    and repo name ``Zomato-Clone``, returns ``blob/main/docs/setup.md``.

    Returns an empty string when there is no subpath.
    """
    # Find the repo name in the URL and grab everything after it.
    lower_url = old_url.lower()
    lower_name = old_repo_name.lower()
    idx = lower_url.find(lower_name)
    if idx == -1:
        return ""
    after = old_url[idx + len(old_repo_name):]
    # Strip leading slash
    return after.lstrip("/")


def _strip_github_prefix(subpath: str) -> str:
    """Remove GitHub blob/tree branch prefixes from *subpath*.

    ``blob/main/docs/setup.md`` → ``docs/setup.md``
    ``tree/master/src``         → ``src``
    """
    parts = PurePosixPath(subpath).parts
    if len(parts) >= 2 and parts[0] in ("blob", "tree"):
        # parts[1] is the branch name — skip both
        return str(PurePosixPath(*parts[2:])) if len(parts) > 2 else ""
    return subpath


def _is_go_file(file_type: str) -> bool:
    return file_type in (".go", ".mod")


def _is_json_metadata_field(context_line: str) -> bool:
    """Return True if the line looks like a JSON metadata field."""
    stripped = context_line.strip().strip(",")
    for key in ("repository", "bugs", "homepage", "url"):
        if f'"{key}"' in stripped:
            return True
    return False


def _target_exists(repo_root: str, consolidated_path: str) -> bool:
    """Check whether *consolidated_path* exists under *repo_root*."""
    full = os.path.join(repo_root, consolidated_path)
    return os.path.exists(full)


def fix_old_url(
    finding: Finding,
    url_map_module: object | None = None,
    repo_root: str = ".",
) -> Replacement | None:
    """Produce a :class:`Replacement` for an ``old_url`` finding.

    Parameters
    ----------
    finding:
        A :class:`Finding` with ``issue_type == "old_url"``.
    url_map_module:
        The URL-map module (defaults to :mod:`tools.repo_consolidation.url_map`).
        Accepts any object exposing ``lookup``, ``resolve_new_path``,
        ``compute_relative_path``, ``CONSOLIDATED_CLONE_URL``, and
        ``CONSOLIDATED_TREE_URL``.
    repo_root:
        Path to the repository root, used for target-existence checks.

    Returns
    -------
    Replacement | None
        A replacement descriptor, or *None* when the old repo name is
        not in the URL map (unmapped finding).
    """
    if url_map_module is None:
        url_map_module = umap

    old_repo_name = finding.old_repo_name
    if not old_repo_name:
        logger.warning("Finding has no old_repo_name: %s", finding)
        return None

    # 1. Look up the consolidated path.
    consolidated_path = url_map_module.lookup(old_repo_name)
    if consolidated_path is None:
        logger.info("Unmapped repo name %r — skipping fix", old_repo_name)
        return None

    context_line = finding.context
    matched_text = finding.matched_text
    source_file = finding.file_path
    file_type = finding.file_type

    # Determine the full old URL from the context line for subpath extraction.
    # The matched_text from the scanner is just the domain/org/repo portion;
    # the actual URL in the line may include a longer path.
    full_old_url = _find_full_url(context_line, old_repo_name)

    # Extract any subpath beyond the repo name (e.g. /blob/main/docs/setup.md).
    raw_subpath = _extract_subpath(full_old_url, old_repo_name)
    clean_subpath = _strip_github_prefix(raw_subpath)

    # Build the target path within the consolidated repo.
    if clean_subpath:
        target_in_repo = f"{consolidated_path}/{clean_subpath}"
    else:
        target_in_repo = consolidated_path

    # Determine whether the target exists on disk.
    target_exists = _target_exists(repo_root, target_in_repo)
    # Also check without subpath if the full target doesn't exist.
    if not target_exists and clean_subpath:
        target_exists = _target_exists(repo_root, consolidated_path)
        # Fall back to just the consolidated path if subpath target missing.
        if target_exists:
            target_in_repo = consolidated_path

    unverified = not target_exists

    # --- Context-aware replacement logic ---

    new_text = context_line
    comment: str | None = None

    # Case 1: Git clone URL
    if _GIT_CLONE_RE.search(context_line):
        new_text = _replace_clone_url(context_line, full_old_url, url_map_module)
        comment = None

    # Case 2: Go import path (in .go or go.mod files)
    elif _is_go_file(file_type):
        new_text = _replace_go_import(
            context_line, old_repo_name, consolidated_path, clean_subpath,
        )

    # Case 3: JSON metadata fields (package.json repository/bugs/homepage)
    elif file_type == ".json" and _is_json_metadata_field(context_line):
        new_text = _replace_json_metadata(
            context_line, full_old_url, consolidated_path, url_map_module,
        )

    # Case 4: Markdown link [text](url)
    elif _MARKDOWN_LINK_RE.search(context_line):
        new_text = _replace_markdown_link(
            context_line, old_repo_name, source_file, target_in_repo,
            url_map_module,
        )

    # Case 5: Default — raw URL in comments, docs, strings, etc.
    else:
        new_text = _replace_raw_url(
            context_line, full_old_url, old_repo_name, source_file,
            target_in_repo, url_map_module,
        )

    if unverified:
        comment = f"# NOTE: target path '{target_in_repo}' could not be verified on disk"

    action = "replace"

    return Replacement(
        file_path=finding.file_path,
        line_number=finding.line_number,
        old_text=context_line,
        new_text=new_text,
        comment=comment,
        action=action,
    )


# ---------------------------------------------------------------------------
# Internal helpers for each replacement context
# ---------------------------------------------------------------------------


def _find_full_url(context_line: str, repo_name: str) -> str:
    """Extract the longest URL containing *repo_name* from *context_line*.

    Falls back to reconstructing a minimal URL if no match is found.
    """
    # Try to grab a full https://github.com/... URL from the line.
    url_re = re.compile(
        r"https?://github\.com/(DevCloudNinjas|devcloudninjas)/"
        + re.escape(repo_name)
        + r"[^\s\)\"'>\]]*",
        re.IGNORECASE,
    )
    m = url_re.search(context_line)
    if m:
        return m.group(0).rstrip("/")

    # Also try without protocol (bare github.com/...)
    bare_re = re.compile(
        r"github\.com/(DevCloudNinjas|devcloudninjas)/"
        + re.escape(repo_name)
        + r"[^\s\)\"'>\]]*",
        re.IGNORECASE,
    )
    m = bare_re.search(context_line)
    if m:
        return m.group(0).rstrip("/")

    return f"github.com/DevCloudNinjas/{repo_name}"


def _replace_clone_url(
    context_line: str,
    full_old_url: str,
    url_map_module: object,
) -> str:
    """Replace a git-clone URL with the consolidated clone URL."""
    clone_url = url_map_module.CONSOLIDATED_CLONE_URL
    # The old URL in a clone command may or may not have .git suffix.
    # Replace the full old URL (with optional .git) with the consolidated one.
    old_with_git = full_old_url.rstrip("/")
    if not old_with_git.endswith(".git"):
        # Try replacing with .git suffix first if present in line
        if old_with_git + ".git" in context_line:
            return context_line.replace(old_with_git + ".git", clone_url)
    return context_line.replace(old_with_git, clone_url)


def _replace_go_import(
    context_line: str,
    old_repo_name: str,
    consolidated_path: str,
    clean_subpath: str,
) -> str:
    """Replace a Go import path with the consolidated repo path."""
    # Go imports use github.com/org/repo/... (no https://)
    # Build the new import path.
    new_import_base = f"github.com/DevCloudNinjas/DevOps-Projects/{consolidated_path}"

    # Match the old import path in the line.
    pattern = re.compile(
        r"github\.com/(DevCloudNinjas|devcloudninjas)/"
        + re.escape(old_repo_name)
        + r"(/[^\s\"']*)?",
        re.IGNORECASE,
    )

    def _repl(m: re.Match[str]) -> str:
        suffix = m.group(2) or ""
        return new_import_base + suffix

    return pattern.sub(_repl, context_line)


def _replace_json_metadata(
    context_line: str,
    full_old_url: str,
    consolidated_path: str,
    url_map_module: object,
) -> str:
    """Replace a JSON metadata URL with the consolidated tree URL."""
    tree_url = url_map_module.CONSOLIDATED_TREE_URL
    new_url = f"{tree_url}/{consolidated_path}"
    return context_line.replace(full_old_url, new_url)


def _replace_markdown_link(
    context_line: str,
    old_repo_name: str,
    source_file: str,
    target_in_repo: str,
    url_map_module: object,
) -> str:
    """Replace old URLs inside markdown link syntax with relative paths."""
    def _repl(m: re.Match[str]) -> str:
        link_text = m.group(1)
        old_url = m.group(2)

        # Extract subpath from this specific URL.
        raw_sub = _extract_subpath(old_url, old_repo_name)
        clean_sub = _strip_github_prefix(raw_sub)

        consolidated_path = url_map_module.lookup(old_repo_name)
        if consolidated_path is None:
            return m.group(0)  # leave unchanged

        if clean_sub:
            target = f"{consolidated_path}/{clean_sub}"
        else:
            target = consolidated_path

        rel_path = url_map_module.compute_relative_path(source_file, target)
        return f"[{link_text}]({rel_path})"

    # Build a pattern that matches markdown links containing the old repo name.
    pattern = re.compile(
        r"\[([^\]]*)\]\((https?://github\.com/(DevCloudNinjas|devcloudninjas)/"
        + re.escape(old_repo_name)
        + r"[^)]*)\)",
        re.IGNORECASE,
    )
    return pattern.sub(_repl, context_line)


def _replace_raw_url(
    context_line: str,
    full_old_url: str,
    old_repo_name: str,
    source_file: str,
    target_in_repo: str,
    url_map_module: object,
) -> str:
    """Replace a raw URL (in comments, docs, strings) with the appropriate path.

    For URLs with ``https://`` prefix, replaces with the consolidated
    tree URL.  For bare ``github.com/...`` references, uses a relative
    path when the source is a documentation file, or the tree URL otherwise.
    """
    consolidated_path = url_map_module.lookup(old_repo_name)
    if consolidated_path is None:
        return context_line

    # Extract subpath for this specific URL occurrence.
    raw_sub = _extract_subpath(full_old_url, old_repo_name)
    clean_sub = _strip_github_prefix(raw_sub)

    if clean_sub:
        target = f"{consolidated_path}/{clean_sub}"
    else:
        target = consolidated_path

    # For full https:// URLs in comments/docs, use the consolidated tree URL.
    if full_old_url.startswith("http"):
        tree_url = url_map_module.CONSOLIDATED_TREE_URL
        new_url = f"{tree_url}/{target}"
        return context_line.replace(full_old_url, new_url)

    # For bare github.com/... references, compute a relative path.
    rel_path = url_map_module.compute_relative_path(source_file, target)
    return context_line.replace(full_old_url, rel_path)


# ---------------------------------------------------------------------------
# Credential fixer
# ---------------------------------------------------------------------------

#: GitHub Personal Access Token pattern.
_PAT_RE = re.compile(r"ghp_[A-Za-z0-9_]{36}")

#: Email address pattern (simple but sufficient for git config contexts).
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

#: Private key file extensions.
_PRIVATE_KEY_EXT_RE = re.compile(r"\.(ppk|pem)$", re.IGNORECASE)


def _is_shell_file(file_type: str) -> bool:
    """Return True if the file type indicates a shell script."""
    return file_type in (".sh", ".bash", ".zsh")


def _is_yaml_file(file_type: str) -> bool:
    """Return True if the file type indicates a YAML file."""
    return file_type in (".yaml", ".yml")


def _is_private_key_file(file_path: str) -> bool:
    """Return True if the file path ends with a private key extension."""
    return bool(_PRIVATE_KEY_EXT_RE.search(file_path))


def _is_credential_only_content(context: str) -> bool:
    """Return True if the context line is essentially credential-only.

    A line is considered credential-only when, after stripping comments
    and whitespace, the remaining content is just a credential value
    (e.g. a bare PAT or a simple ``key=PAT`` assignment with no other
    functional code).
    """
    stripped = context.strip()
    if not stripped or stripped.startswith("#"):
        return False
    # Check if the entire meaningful content is just a PAT
    if _PAT_RE.fullmatch(stripped):
        return True
    return False


def fix_credential(finding: Finding) -> Replacement:
    """Produce a :class:`Replacement` for a ``credential`` finding.

    Parameters
    ----------
    finding:
        A :class:`Finding` with ``issue_type == "credential"``.

    Returns
    -------
    Replacement
        A replacement descriptor indicating how to remediate the
        credential.  The ``action`` field is set to ``replace`` for
        inline credential replacement, ``delete_file`` or
        ``flag_for_review`` for private key files or credential-only
        files.

    Requirements: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
    """
    file_path = finding.file_path
    file_type = finding.file_type
    context_line = finding.context
    matched_text = finding.matched_text

    # --- Case 1: Private key files (.ppk, .pem) — flag for review/deletion ---
    if _is_private_key_file(file_path):
        return Replacement(
            file_path=file_path,
            line_number=finding.line_number,
            old_text=context_line,
            new_text="",
            comment="Private key file should be removed from the repository",
            action="flag_for_review",
        )

    # --- Case 2: PAT in shell scripts — replace with $GITHUB_TOKEN ---
    if _PAT_RE.search(matched_text) and _is_shell_file(file_type):
        new_text = _PAT_RE.sub("$GITHUB_TOKEN", context_line)
        return Replacement(
            file_path=file_path,
            line_number=finding.line_number,
            old_text=context_line,
            new_text=new_text,
            comment="# Set GITHUB_TOKEN environment variable",
            action="replace",
        )

    # --- Case 3: PAT in YAML workflows — replace with ${{ secrets.GITHUB_TOKEN }} ---
    if _PAT_RE.search(matched_text) and _is_yaml_file(file_type):
        new_text = _PAT_RE.sub("${{ secrets.GITHUB_TOKEN }}", context_line)
        return Replacement(
            file_path=file_path,
            line_number=finding.line_number,
            old_text=context_line,
            new_text=new_text,
            comment="# Use GitHub Actions secret for authentication",
            action="replace",
        )

    # --- Case 4: PAT in other file types — replace with $GITHUB_TOKEN ---
    if _PAT_RE.search(matched_text):
        new_text = _PAT_RE.sub("$GITHUB_TOKEN", context_line)
        return Replacement(
            file_path=file_path,
            line_number=finding.line_number,
            old_text=context_line,
            new_text=new_text,
            comment="# Set GITHUB_TOKEN environment variable",
            action="replace",
        )

    # --- Case 5: Email addresses — replace with placeholder ---
    if _EMAIL_RE.search(matched_text):
        new_text = _EMAIL_RE.sub("<EMAIL>", context_line)
        return Replacement(
            file_path=file_path,
            line_number=finding.line_number,
            old_text=context_line,
            new_text=new_text,
            comment=None,
            action="replace",
        )

    # --- Case 6: Credential-only file content — flag for deletion ---
    if _is_credential_only_content(context_line):
        return Replacement(
            file_path=file_path,
            line_number=finding.line_number,
            old_text=context_line,
            new_text="",
            comment="File contains only credential content — consider deletion",
            action="delete_file",
        )

    # --- Fallback: generic credential replacement ---
    # For any other credential finding, replace the matched text with a
    # placeholder and add a comment.
    new_text = context_line.replace(matched_text, "<CREDENTIAL>")
    return Replacement(
        file_path=file_path,
        line_number=finding.line_number,
        old_text=context_line,
        new_text=new_text,
        comment="# Credential removed — set appropriate environment variable",
        action="replace",
    )

# ---------------------------------------------------------------------------
# Account ID fixer
# ---------------------------------------------------------------------------

#: ECR registry URL pattern: 12-digit account ID, region, optional image path.
_ECR_URL_RE = re.compile(
    r"\d{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com(/[^\s\"',:]+)?",
)


def fix_account_id(finding: Finding) -> Replacement:
    """Produce a :class:`Replacement` for a ``hardcoded_account_id`` finding.

    Parameters
    ----------
    finding:
        A :class:`Finding` with ``issue_type == "hardcoded_account_id"``.

    Returns
    -------
    Replacement
        A replacement descriptor that substitutes the 12-digit AWS
        account ID with ``<AWS_ACCOUNT_ID>`` and any trailing image
        name with ``<IMAGE_NAME>``.

    Requirements: 6.2, 6.3, 6.4
    """
    context_line = finding.context

    def _replace_ecr(m: re.Match[str]) -> str:
        full = m.group(0)
        image_suffix = m.group(1)  # e.g. "/devcloudninjas" or None
        # Replace the 12-digit account ID with placeholder.
        replaced = re.sub(r"\d{12}", "<AWS_ACCOUNT_ID>", full, count=1)
        # Replace image name portion if present.
        if image_suffix:
            replaced = re.sub(re.escape(image_suffix), "/<IMAGE_NAME>", replaced, count=1)
        return replaced

    new_text = _ECR_URL_RE.sub(_replace_ecr, context_line)

    return Replacement(
        file_path=finding.file_path,
        line_number=finding.line_number,
        old_text=context_line,
        new_text=new_text,
        comment="# Replace <AWS_ACCOUNT_ID> with your AWS account ID",
        action="replace",
    )

# ---------------------------------------------------------------------------
# Go module fixer
# ---------------------------------------------------------------------------


def fix_go_module(
    finding: Finding,
    url_map_module: object | None = None,
    repo_root: str = ".",
) -> list[Replacement]:
    """Fix a ``go.mod`` module declaration and update sibling Go source files.

    When a ``go.mod`` file declares a module path referencing an old
    standalone repo (e.g. ``github.com/devcloudninjas/devops-bootcamp/...``),
    this function:

    1. Updates the ``module`` directive in ``go.mod`` to use the
       consolidated repo path.
    2. Scans ``require`` directives in the same ``go.mod`` for old repo
       references and updates them.
    3. Walks sibling ``.go`` files in the same module directory tree and
       updates any import paths that reference the old module path.

    Parameters
    ----------
    finding:
        A :class:`Finding` for a ``go.mod`` file with ``issue_type == "old_url"``.
    url_map_module:
        The URL-map module (defaults to :mod:`tools.repo_consolidation.url_map`).
    repo_root:
        Path to the repository root.

    Returns
    -------
    list[Replacement]
        One or more replacements — the first for the ``go.mod`` file itself,
        followed by any Go source files that need import path updates.

    Requirements: 7.2, 7.3, 7.4, 8.4
    """
    if url_map_module is None:
        url_map_module = umap

    old_repo_name = finding.old_repo_name
    if not old_repo_name:
        return []

    consolidated_path = url_map_module.lookup(old_repo_name)
    if consolidated_path is None:
        return []

    replacements: list[Replacement] = []

    # --- 1. Fix the go.mod file itself ---
    gomod_path = os.path.join(repo_root, finding.file_path)
    new_import_base = f"github.com/DevCloudNinjas/DevOps-Projects/{consolidated_path}"

    # Build regex to match old module/import paths in go.mod
    old_import_pattern = re.compile(
        r"github\.com/(DevCloudNinjas|devcloudninjas)/"
        + re.escape(old_repo_name)
        + r"(/[^\s\"']*)?",
        re.IGNORECASE,
    )

    # Read the full go.mod content and update all matching lines
    try:
        with open(gomod_path, encoding="utf-8") as fh:
            gomod_lines = fh.readlines()
    except OSError:
        # If we can't read the file, just fix the single finding line
        new_text = _replace_go_import(
            finding.context, old_repo_name, consolidated_path, "",
        )
        replacements.append(Replacement(
            file_path=finding.file_path,
            line_number=finding.line_number,
            old_text=finding.context,
            new_text=new_text,
            comment=None,
            action="replace",
        ))
        return replacements

    for line_no, line in enumerate(gomod_lines, start=1):
        line_stripped = line.rstrip("\n")
        if old_import_pattern.search(line_stripped):
            new_line = _replace_go_import(
                line_stripped, old_repo_name, consolidated_path, "",
            )
            replacements.append(Replacement(
                file_path=finding.file_path,
                line_number=line_no,
                old_text=line_stripped,
                new_text=new_line,
                comment=None,
                action="replace",
            ))

    # --- 2. Scan sibling .go files for import paths referencing the old module ---
    gomod_abs_dir = os.path.dirname(gomod_path)
    if os.path.isdir(gomod_abs_dir):
        for dirpath, _dirnames, filenames in os.walk(gomod_abs_dir):
            for fname in filenames:
                if not fname.endswith(".go"):
                    continue
                go_file_abs = os.path.join(dirpath, fname)
                try:
                    with open(go_file_abs, encoding="utf-8") as fh:
                        go_lines = fh.readlines()
                except OSError:
                    continue

                # Compute relative path from repo root
                go_file_rel = os.path.relpath(go_file_abs, repo_root).replace("\\", "/")

                for go_line_no, go_line in enumerate(go_lines, start=1):
                    go_line_stripped = go_line.rstrip("\n")
                    if old_import_pattern.search(go_line_stripped):
                        new_go_line = _replace_go_import(
                            go_line_stripped, old_repo_name,
                            consolidated_path, "",
                        )
                        replacements.append(Replacement(
                            file_path=go_file_rel,
                            line_number=go_line_no,
                            old_text=go_line_stripped,
                            new_text=new_go_line,
                            comment=None,
                            action="replace",
                        ))

    return replacements


# ---------------------------------------------------------------------------
# Docker image fixer
# ---------------------------------------------------------------------------

#: Pattern matching docker.build("devcloudninjas") calls in Jenkinsfiles.
_DOCKER_BUILD_RE = re.compile(
    r'(docker\.build\(["\'])devcloudninjas(["\'])',
    re.IGNORECASE,
)

#: Standalone "devcloudninjas" image name (not part of a URL or docker.build).
#: Mirrors the scanner's _DOCKER_IMAGE_NAME_PATTERN — excludes emails,
#: domain names, possessives, and other non-Docker contexts.
_STANDALONE_IMAGE_RE = re.compile(
    r"(?<![/\w@])devcloudninjas(?![/\w@'.])",
    re.IGNORECASE,
)


def fix_docker_image(finding: Finding) -> Replacement:
    """Produce a :class:`Replacement` for a ``stale_docker_image`` finding.

    Parameters
    ----------
    finding:
        A :class:`Finding` with ``issue_type == "stale_docker_image"``.

    Returns
    -------
    Replacement
        A replacement descriptor that substitutes the hardcoded
        ``devcloudninjas`` Docker image name with ``<IMAGE_NAME>``.

    Requirements: 4.4
    """
    context_line = finding.context

    # Case 1: docker.build("devcloudninjas") → docker.build("<IMAGE_NAME>")
    if _DOCKER_BUILD_RE.search(context_line):
        new_text = _DOCKER_BUILD_RE.sub(r"\1<IMAGE_NAME>\2", context_line)
    else:
        # Case 2: standalone image name (e.g. YAML image field)
        new_text = _STANDALONE_IMAGE_RE.sub("<IMAGE_NAME>", context_line)

    return Replacement(
        file_path=finding.file_path,
        line_number=finding.line_number,
        old_text=context_line,
        new_text=new_text,
        comment=None,
        action="replace",
    )
# ---------------------------------------------------------------------------
# Go module fixer
# ---------------------------------------------------------------------------


def fix_go_module(
    finding: Finding,
    url_map_module: object | None = None,
    repo_root: str = ".",
) -> list[Replacement]:
    """Fix a ``go.mod`` module declaration and update sibling Go source files.

    When a ``go.mod`` file declares a module path referencing an old
    standalone repo (e.g. ``github.com/devcloudninjas/devops-bootcamp/...``),
    this function:

    1. Updates the ``module`` directive in ``go.mod`` to use the
       consolidated repo path.
    2. Scans ``require`` directives in the same ``go.mod`` for old repo
       references and updates them.
    3. Walks sibling ``.go`` files in the same module directory tree and
       updates any import paths that reference the old module path.

    Parameters
    ----------
    finding:
        A :class:`Finding` for a ``go.mod`` file with ``issue_type == "old_url"``.
    url_map_module:
        The URL-map module (defaults to :mod:`tools.repo_consolidation.url_map`).
    repo_root:
        Path to the repository root.

    Returns
    -------
    list[Replacement]
        One or more replacements — the first for the ``go.mod`` file itself,
        followed by any Go source files that need import path updates.

    Requirements: 7.2, 7.3, 7.4, 8.4
    """
    if url_map_module is None:
        url_map_module = umap

    old_repo_name = finding.old_repo_name
    if not old_repo_name:
        return []

    consolidated_path = url_map_module.lookup(old_repo_name)
    if consolidated_path is None:
        return []

    replacements: list[Replacement] = []

    # --- 1. Fix the go.mod file itself ---
    gomod_path = os.path.join(repo_root, finding.file_path)
    gomod_dir = os.path.dirname(finding.file_path)

    new_import_base = f"github.com/DevCloudNinjas/DevOps-Projects/{consolidated_path}"

    # Build regex to match old module/import paths in go.mod
    old_import_pattern = re.compile(
        r"github\.com/(DevCloudNinjas|devcloudninjas)/"
        + re.escape(old_repo_name)
        + r"(/[^\s\"']*)?",
        re.IGNORECASE,
    )

    # Read the full go.mod content and update all matching lines
    try:
        with open(gomod_path, encoding="utf-8") as fh:
            gomod_lines = fh.readlines()
    except OSError:
        # If we can't read the file, just fix the single finding line
        new_text = _replace_go_import(
            finding.context, old_repo_name, consolidated_path, "",
        )
        replacements.append(Replacement(
            file_path=finding.file_path,
            line_number=finding.line_number,
            old_text=finding.context,
            new_text=new_text,
            comment=None,
            action="replace",
        ))
        return replacements

    for line_no, line in enumerate(gomod_lines, start=1):
        line_stripped = line.rstrip("\n")
        if old_import_pattern.search(line_stripped):
            new_line = _replace_go_import(
                line_stripped, old_repo_name, consolidated_path, "",
            )
            replacements.append(Replacement(
                file_path=finding.file_path,
                line_number=line_no,
                old_text=line_stripped,
                new_text=new_line,
                comment=None,
                action="replace",
            ))

    # --- 2. Scan sibling .go files for import paths referencing the old module ---
    gomod_abs_dir = os.path.dirname(gomod_path)
    if os.path.isdir(gomod_abs_dir):
        for dirpath, _dirnames, filenames in os.walk(gomod_abs_dir):
            for fname in filenames:
                if not fname.endswith(".go"):
                    continue
                go_file_abs = os.path.join(dirpath, fname)
                try:
                    with open(go_file_abs, encoding="utf-8") as fh:
                        go_lines = fh.readlines()
                except OSError:
                    continue

                # Compute relative path from repo root
                go_file_rel = os.path.relpath(go_file_abs, repo_root).replace("\\", "/")

                for go_line_no, go_line in enumerate(go_lines, start=1):
                    go_line_stripped = go_line.rstrip("\n")
                    if old_import_pattern.search(go_line_stripped):
                        new_go_line = _replace_go_import(
                            go_line_stripped, old_repo_name,
                            consolidated_path, "",
                        )
                        replacements.append(Replacement(
                            file_path=go_file_rel,
                            line_number=go_line_no,
                            old_text=go_line_stripped,
                            new_text=new_go_line,
                            comment=None,
                            action="replace",
                        ))

    return replacements


