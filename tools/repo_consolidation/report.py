"""Report generator for the repo consolidation remediation pipeline.

Produces human-readable summary and unresolved-issues reports from
scan results and validation data.
"""

from __future__ import annotations

from collections import Counter

from .models import Finding, ValidationReport


def generate_report(
    scan_results: list[Finding],
    validation: ValidationReport,
) -> str:
    """Produce a formatted summary report.

    The report includes:
    - Header
    - Files scanned by type
    - Fix summary (references fixed, credentials removed, account IDs
      parameterized)
    - Validation results (links validated, broken paths, remaining issues)
    - Unresolved issues detail (if any remain)

    Args:
        scan_results: Findings from the initial scan pass.
        validation: The :class:`ValidationReport` produced after fixes.

    Returns:
        A multi-line formatted string suitable for display or file output.
    """
    lines: list[str] = []

    # -- Header ---------------------------------------------------------------
    lines.append("=" * 60)
    lines.append("Repo Consolidation — Remediation Report")
    lines.append("=" * 60)
    lines.append("")

    # -- Files scanned by type ------------------------------------------------
    lines.append("Files Scanned by Type")
    lines.append("-" * 40)
    if validation.total_files_scanned:
        for ext in sorted(validation.total_files_scanned):
            lines.append(f"  {ext}: {validation.total_files_scanned[ext]}")
    else:
        lines.append("  (none)")
    lines.append("")

    # -- Initial scan summary -------------------------------------------------
    type_counts = Counter(f.issue_type for f in scan_results)
    lines.append("Initial Scan Summary")
    lines.append("-" * 40)
    lines.append(f"  Total issues found: {len(scan_results)}")
    for issue_type in sorted(type_counts):
        lines.append(f"    {issue_type}: {type_counts[issue_type]}")
    lines.append("")

    # -- Fix summary ----------------------------------------------------------
    lines.append("Fix Summary")
    lines.append("-" * 40)
    lines.append(f"  References fixed:        {validation.total_references_fixed}")
    lines.append(f"  Credentials removed:     {validation.total_credentials_removed}")
    lines.append(f"  Account IDs parameterized: {validation.total_account_ids_parameterized}")
    lines.append("")

    # -- Validation results ---------------------------------------------------
    lines.append("Validation Results")
    lines.append("-" * 40)
    lines.append(f"  Links validated:         {validation.total_links_validated}")
    lines.append(f"  Broken relative paths:   {validation.total_broken_relative_paths}")
    lines.append(f"  Remaining issues:        {len(validation.remaining_issues)}")
    lines.append("")

    # -- Unresolved issues (inline) -------------------------------------------
    if validation.remaining_issues:
        lines.append(_format_unresolved_section(validation.remaining_issues))

    lines.append("=" * 60)
    return "\n".join(lines)


def generate_unresolved_report(validation: ValidationReport) -> str:
    """Produce a detailed listing of remaining (unresolved) issues.

    Args:
        validation: The :class:`ValidationReport` produced after fixes.

    Returns:
        A multi-line formatted string listing every remaining issue,
        or a short "no issues" message when the list is empty.
    """
    if not validation.remaining_issues:
        return "No unresolved issues."

    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("Unresolved Issues Report")
    lines.append("=" * 60)
    lines.append("")
    lines.append(_format_unresolved_section(validation.remaining_issues))
    lines.append("=" * 60)
    return "\n".join(lines)


def _format_unresolved_section(issues: list[Finding]) -> str:
    """Format a list of findings into a readable unresolved-issues block.

    Issues are grouped by file path for easier review.
    """
    lines: list[str] = []
    lines.append("Unresolved Issues")
    lines.append("-" * 40)

    # Group by file path for readability
    by_file: dict[str, list[Finding]] = {}
    for f in issues:
        by_file.setdefault(f.file_path, []).append(f)

    for file_path in sorted(by_file):
        lines.append(f"  {file_path}")
        for finding in sorted(by_file[file_path], key=lambda f: f.line_number):
            lines.append(
                f"    Line {finding.line_number}: [{finding.issue_type}] "
                f"{finding.matched_text}"
            )
        lines.append("")

    return "\n".join(lines)
