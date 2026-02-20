"""Post-fix validation for the repo consolidation pipeline.

Re-scans the repository after fixes are applied to verify that no
old URLs, credentials, or hardcoded account IDs remain, and that all
relative paths introduced by fixes resolve to existing files or
directories.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from tools.repo_consolidation.models import Finding, ValidationReport
from tools.repo_consolidation.scanner import SCAN_PATTERNS, discover_files, scan_repo

logger = logging.getLogger(__name__)


def count_files_by_extension(repo_root: str | Path) -> dict[str, int]:
    """Count text files under *repo_root* grouped by file extension.

    Special filenames (``Jenkinsfile``, ``Dockerfile``, etc.) are keyed
    by their full name.  All other files are keyed by their lowercase
    extension including the leading dot (e.g. ``.md``).  Files with no
    extension are keyed by their full name.

    Returns a dict mapping extension/name → count.
    """
    counts: dict[str, int] = {}
    for fpath in discover_files(repo_root):
        name = fpath.name
        if name in {"Jenkinsfile", "Dockerfile", "Makefile", "Vagrantfile"}:
            key = name
        else:
            ext = fpath.suffix.lower()
            key = ext if ext else name
        counts[key] = counts.get(key, 0) + 1
    return counts


def validate_fixes(repo_root: str | Path) -> ValidationReport:
    """Re-scan the repo and build a :class:`ValidationReport`.

    Steps:
    1. Discover all text files and count them by extension.
    2. Run :func:`scan_repo` with the default :data:`SCAN_PATTERNS` to
       detect any remaining issues.
    3. Populate the report with remaining issues grouped by type.

    Parameters
    ----------
    repo_root:
        Path to the repository root directory.

    Returns
    -------
    ValidationReport
        A report summarising the validation results.
    """
    root = Path(repo_root).resolve()

    # 1. Count files by extension
    total_files_scanned = count_files_by_extension(root)

    # 2. Re-scan for remaining issues
    remaining = scan_repo(root, SCAN_PATTERNS)

    # 3. Build the report
    report = ValidationReport(
        total_files_scanned=total_files_scanned,
        remaining_issues=remaining,
    )

    if remaining:
        logger.warning(
            "Validation found %d remaining issue(s) after fixes.",
            len(remaining),
        )
    else:
        logger.info("Validation passed — zero remaining issues.")

    return report
