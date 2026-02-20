"""Core data models for the repo consolidation remediation pipeline.

Defines the dataclasses used across all pipeline stages: scanning,
classification, fixing, validation, and reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Finding:
    """A single issue detected by the scanner.

    Attributes:
        file_path: Relative path from repo root to the file containing the issue.
        line_number: 1-based line number where the issue was found.
        matched_text: The exact text that matched a scan pattern.
        issue_type: Category of the issue — one of ``old_url``,
            ``credential``, ``hardcoded_account_id``, or ``stale_docker_image``.
        old_repo_name: Extracted old repository name (primarily for ``old_url`` type).
        context: Full line content for human review.
        file_type: File extension (e.g. ``.md``, ``.yaml``) or special filename
            (e.g. ``Jenkinsfile``).
    """

    file_path: str
    line_number: int
    matched_text: str
    issue_type: str
    old_repo_name: str
    context: str
    file_type: str


@dataclass
class Replacement:
    """A proposed or applied fix for a single finding.

    Attributes:
        file_path: Relative path from repo root to the file to modify.
        line_number: 1-based line number of the text to replace.
        old_text: The original text to be replaced.
        new_text: The replacement text.
        comment: Optional comment to insert above the modified line.
        action: The kind of fix — ``replace``, ``delete_file``, or
            ``flag_for_review``.
    """

    file_path: str
    line_number: int
    old_text: str
    new_text: str
    comment: str | None = None
    action: str = "replace"


@dataclass
class RepoMapping:
    """Maps an old standalone repo to its location in the consolidated repo.

    Attributes:
        old_repo_name: Original repository name (e.g. ``Zomato-Clone``).
        old_url_patterns: URL pattern variants including case differences.
        new_consolidated_path: Target path inside the consolidated repo
            (e.g. ``project-13-zomato-clone-devsecops``).
        is_learning: ``True`` if the repo was merged into the ``learning/`` tree.
        is_resource: ``True`` if the repo was merged into the ``resources/`` tree.
    """

    old_repo_name: str
    old_url_patterns: list[str]
    new_consolidated_path: str
    is_learning: bool = False
    is_resource: bool = False


@dataclass
class ScanConfig:
    """Configuration for a scanning run.

    Attributes:
        repo_root: Absolute or relative path to the repository root.
        file_extensions: File extensions to scan (e.g. ``[".md", ".go"]``).
        special_filenames: Exact filenames to scan regardless of extension
            (e.g. ``["Jenkinsfile", "Dockerfile"]``).
        skip_dirs: Directory names to skip during traversal
            (e.g. ``[".git", "node_modules"]``).
        patterns: Mapping of issue type to its regex pattern string.
    """

    repo_root: str
    file_extensions: list[str] = field(default_factory=list)
    special_filenames: list[str] = field(default_factory=list)
    skip_dirs: list[str] = field(default_factory=list)
    patterns: dict[str, str] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Results of the post-fix validation pass.

    Attributes:
        total_files_scanned: Count of files scanned, keyed by file extension.
        total_references_fixed: Number of old URL references that were fixed.
        total_credentials_removed: Number of credentials removed.
        total_account_ids_parameterized: Number of hardcoded account IDs replaced.
        total_links_validated: Number of relative links verified as resolving.
        total_broken_relative_paths: Number of relative paths that do not resolve.
        remaining_issues: Findings that still exist after all fixes were applied.
    """

    total_files_scanned: dict[str, int] = field(default_factory=dict)
    total_references_fixed: int = 0
    total_credentials_removed: int = 0
    total_account_ids_parameterized: int = 0
    total_links_validated: int = 0
    total_broken_relative_paths: int = 0
    remaining_issues: list[Finding] = field(default_factory=list)
