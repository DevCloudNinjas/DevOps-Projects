"""Replacement application engine for the repo consolidation pipeline.

Applies ``Replacement`` objects to files on disk, supporting dry-run mode,
multiple replacements per file (applied in reverse line order to preserve
line numbers), and the ``replace``, ``delete_file``, and ``flag_for_review``
actions.
"""

from __future__ import annotations

import logging
import os
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .models import Replacement

logger = logging.getLogger(__name__)


@dataclass
class ApplySummary:
    """Summary of changes applied (or proposed in dry-run mode).

    Attributes:
        files_modified: Number of files that had lines replaced.
        files_deleted: Number of files deleted.
        files_flagged: Number of files flagged for manual review.
        replacements_applied: Total line-level replacements applied.
        errors: List of error messages for operations that failed.
    """

    files_modified: int = 0
    files_deleted: int = 0
    files_flagged: int = 0
    replacements_applied: int = 0
    errors: list[str] = field(default_factory=list)


def apply_replacements(
    replacements: list[Replacement],
    repo_root: str,
    *,
    dry_run: bool = False,
) -> ApplySummary:
    """Apply a list of replacements to files on disk.

    Replacements are grouped by file path, then sorted in reverse line-number
    order so that earlier line numbers are not shifted by later edits.

    Args:
        replacements: The replacement objects to apply.
        repo_root: Absolute or relative path to the repository root.
        dry_run: If ``True``, log proposed changes without writing to disk.

    Returns:
        An :class:`ApplySummary` describing what was (or would be) changed.
    """
    summary = ApplySummary()
    root = Path(repo_root)

    grouped: dict[str, list[Replacement]] = defaultdict(list)
    for r in replacements:
        grouped[r.file_path].append(r)

    for file_path, file_replacements in grouped.items():
        _apply_file_replacements(file_replacements, file_path, root, dry_run, summary)

    return summary


def _apply_file_replacements(
    file_replacements: list[Replacement],
    file_path: str,
    root: Path,
    dry_run: bool,
    summary: ApplySummary,
) -> None:
    """Process all replacements for a single file."""
    # Separate by action type
    delete_actions = [r for r in file_replacements if r.action == "delete_file"]
    flag_actions = [r for r in file_replacements if r.action == "flag_for_review"]
    replace_actions = [r for r in file_replacements if r.action == "replace"]

    # Handle flag_for_review first (no file modification)
    for r in flag_actions:
        logger.warning(
            "FLAG FOR REVIEW: %s (line %d): %s",
            file_path,
            r.line_number,
            r.old_text.rstrip("\n"),
        )
        summary.files_flagged += 1

    # Handle delete_file
    if delete_actions:
        _handle_delete(file_path, root, dry_run, summary)
        return  # no point applying line replacements to a deleted file

    # Handle line-level replacements
    if replace_actions:
        _handle_replacements(replace_actions, file_path, root, dry_run, summary)


def _handle_delete(
    file_path: str,
    root: Path,
    dry_run: bool,
    summary: ApplySummary,
) -> None:
    """Delete a file or log the proposed deletion in dry-run mode."""
    abs_path = root / file_path
    if dry_run:
        logger.info("DRY-RUN: would delete %s", file_path)
    else:
        try:
            abs_path.unlink()
            logger.info("Deleted %s", file_path)
        except FileNotFoundError:
            msg = f"File not found for deletion: {file_path}"
            logger.error(msg)
            summary.errors.append(msg)
            return
        except OSError as exc:
            msg = f"Failed to delete {file_path}: {exc}"
            logger.error(msg)
            summary.errors.append(msg)
            return
    summary.files_deleted += 1


def _handle_replacements(
    replace_actions: list[Replacement],
    file_path: str,
    root: Path,
    dry_run: bool,
    summary: ApplySummary,
) -> None:
    """Apply line-level replacements to a single file."""
    abs_path = root / file_path

    try:
        lines = abs_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except FileNotFoundError:
        msg = f"File not found for replacement: {file_path}"
        logger.error(msg)
        summary.errors.append(msg)
        return
    except OSError as exc:
        msg = f"Failed to read {file_path}: {exc}"
        logger.error(msg)
        summary.errors.append(msg)
        return

    # Sort by line_number descending so earlier indices stay valid
    sorted_replacements = sorted(replace_actions, key=lambda r: r.line_number, reverse=True)

    applied_count = 0
    for r in sorted_replacements:
        idx = r.line_number - 1  # convert 1-based to 0-based
        if idx < 0 or idx >= len(lines):
            msg = (
                f"Line {r.line_number} out of range in {file_path} "
                f"(file has {len(lines)} lines)"
            )
            logger.error(msg)
            summary.errors.append(msg)
            continue

        if dry_run:
            logger.info(
                "DRY-RUN: %s line %d: %r -> %r",
                file_path,
                r.line_number,
                r.old_text.rstrip("\n"),
                r.new_text.rstrip("\n"),
            )
        else:
            # Replace the line content
            lines[idx] = r.new_text if r.new_text.endswith("\n") else r.new_text + "\n"

            # Insert comment above the modified line if specified
            if r.comment:
                comment_line = r.comment if r.comment.endswith("\n") else r.comment + "\n"
                lines.insert(idx, comment_line)

        applied_count += 1

    if applied_count > 0:
        if not dry_run:
            try:
                abs_path.write_text("".join(lines), encoding="utf-8")
            except OSError as exc:
                msg = f"Failed to write {file_path}: {exc}"
                logger.error(msg)
                summary.errors.append(msg)
                return
        summary.files_modified += 1
        summary.replacements_applied += applied_count
