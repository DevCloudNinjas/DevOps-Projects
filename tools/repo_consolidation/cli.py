"""CLI entry point for the repo consolidation remediation pipeline.

Usage:
    python -m tools.repo_consolidation <repo_root> [--dry-run] [--report-output PATH] [--verbose]
"""

import argparse
import logging
import sys
from pathlib import Path

from tools.repo_consolidation.applier import apply_replacements
from tools.repo_consolidation.fixers import (
    fix_account_id,
    fix_credential,
    fix_docker_image,
    fix_old_url,
)
from tools.repo_consolidation.models import Replacement
from tools.repo_consolidation.report import generate_report
from tools.repo_consolidation.scanner import scan_repo
from tools.repo_consolidation.validator import validate_fixes


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="repo-consolidation",
        description=(
            "Scan a consolidated DevOps repo for broken URLs, exposed "
            "credentials, hardcoded AWS account IDs, and stale Docker "
            "image names — then fix them in place and validate the results."
        ),
    )
    parser.add_argument(
        "repo_root",
        type=str,
        help="Path to the root of the consolidated repository to scan.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Log proposed changes without writing to disk.",
    )
    parser.add_argument(
        "--report-output",
        type=str,
        default=None,
        help="File path to write the remediation report to.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable detailed logging output.",
    )
    return parser


def configure_logging(verbose: bool) -> None:
    """Configure logging based on verbosity flag."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run the remediation pipeline.

    Stages: scan → classify → fix → apply → validate → report.
    Returns 0 on success, 1 on errors.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(args.verbose)
    logger = logging.getLogger(__name__)

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        logger.error("Repo root does not exist or is not a directory: %s", repo_root)
        return 1

    logger.info("Repo root: %s", repo_root)
    logger.info("Dry-run: %s", args.dry_run)
    if args.report_output:
        logger.info("Report output: %s", args.report_output)

    repo_root_str = str(repo_root)

    # --- Stage 1: Scan -------------------------------------------------------
    logger.info("Stage 1: Scanning repository...")
    try:
        findings = scan_repo(repo_root_str)
    except Exception:
        logger.exception("Fatal error during scan stage")
        return 1

    logger.info("Scan complete — %d finding(s) detected.", len(findings))

    # --- Stage 2: Classify (already done by scanner via issue_type) -----------
    # Findings are pre-classified by the scanner into issue_type categories.

    # --- Stage 3: Fix — produce Replacement objects --------------------------
    logger.info("Stage 3: Generating fixes...")
    replacements: list[Replacement] = []
    fixer_map = {
        "old_url": lambda f: fix_old_url(f, repo_root=repo_root_str),
        "credential": fix_credential,
        "hardcoded_account_id": fix_account_id,
        "stale_docker_image": fix_docker_image,
    }

    for finding in findings:
        fixer = fixer_map.get(finding.issue_type)
        if fixer is None:
            logger.warning(
                "No fixer for issue type %r in %s:%d — skipping",
                finding.issue_type,
                finding.file_path,
                finding.line_number,
            )
            continue
        try:
            replacement = fixer(finding)
            if replacement is not None:
                replacements.append(replacement)
            else:
                logger.debug(
                    "Fixer returned None for %s:%d (%s) — unmapped or skipped",
                    finding.file_path,
                    finding.line_number,
                    finding.issue_type,
                )
        except Exception:
            logger.exception(
                "Error fixing %s:%d (%s) — skipping",
                finding.file_path,
                finding.line_number,
                finding.issue_type,
            )

    logger.info("Generated %d replacement(s).", len(replacements))

    # --- Stage 4: Apply replacements -----------------------------------------
    logger.info("Stage 4: Applying replacements (dry_run=%s)...", args.dry_run)
    try:
        apply_summary = apply_replacements(
            replacements, repo_root_str, dry_run=args.dry_run,
        )
    except Exception:
        logger.exception("Fatal error during apply stage")
        return 1

    logger.info(
        "Apply complete — %d file(s) modified, %d file(s) deleted, "
        "%d file(s) flagged, %d replacement(s) applied.",
        apply_summary.files_modified,
        apply_summary.files_deleted,
        apply_summary.files_flagged,
        apply_summary.replacements_applied,
    )
    if apply_summary.errors:
        for err in apply_summary.errors:
            logger.error("Apply error: %s", err)

    # --- Stage 5: Validate ---------------------------------------------------
    logger.info("Stage 5: Validating fixes...")
    try:
        validation = validate_fixes(repo_root_str)
    except Exception:
        logger.exception("Fatal error during validation stage")
        return 1

    # Populate summary counts from the apply stage.
    _count_by_type: dict[str, int] = {}
    for f in findings:
        _count_by_type[f.issue_type] = _count_by_type.get(f.issue_type, 0) + 1

    validation.total_references_fixed = _count_by_type.get("old_url", 0)
    validation.total_credentials_removed = _count_by_type.get("credential", 0)
    validation.total_account_ids_parameterized = _count_by_type.get(
        "hardcoded_account_id", 0,
    )
    validation.total_links_validated = apply_summary.replacements_applied

    logger.info(
        "Validation complete — %d remaining issue(s).",
        len(validation.remaining_issues),
    )

    # --- Stage 6: Report -----------------------------------------------------
    logger.info("Stage 6: Generating report...")
    report_text = generate_report(findings, validation)

    print(report_text)

    if args.report_output:
        try:
            report_path = Path(args.report_output)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(report_text, encoding="utf-8")
            logger.info("Report written to %s", args.report_output)
        except OSError:
            logger.exception("Failed to write report to %s", args.report_output)

    # Return 1 if there were apply errors or remaining issues.
    has_errors = bool(apply_summary.errors) or bool(validation.remaining_issues)
    return 1 if has_errors else 0



if __name__ == "__main__":
    sys.exit(main())
