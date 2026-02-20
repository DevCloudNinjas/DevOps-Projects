"""Tests for the replacement application engine."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from tools.repo_consolidation.applier import ApplySummary, apply_replacements
from tools.repo_consolidation.models import Replacement


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_file(tmp_path: Path, rel: str, content: str) -> Path:
    """Write *content* to *tmp_path / rel* and return the absolute path."""
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Basic replace action
# ---------------------------------------------------------------------------

class TestReplaceAction:
    """Tests for the ``replace`` action."""

    def test_single_replacement(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "README.md", "line1\nold line\nline3\n")
        r = Replacement("README.md", 2, "old line", "new line", action="replace")
        summary = apply_replacements([r], str(tmp_path))

        assert (tmp_path / "README.md").read_text() == "line1\nnew line\nline3\n"
        assert summary.replacements_applied == 1
        assert summary.files_modified == 1

    def test_multiple_replacements_same_file(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "a\nb\nc\nd\n")
        replacements = [
            Replacement("f.txt", 2, "b", "B", action="replace"),
            Replacement("f.txt", 4, "d", "D", action="replace"),
        ]
        summary = apply_replacements(replacements, str(tmp_path))

        assert (tmp_path / "f.txt").read_text() == "a\nB\nc\nD\n"
        assert summary.replacements_applied == 2
        assert summary.files_modified == 1

    def test_reverse_order_preserves_line_numbers(self, tmp_path: Path) -> None:
        """Replacements on lines 1 and 3 with comments should not shift."""
        _write_file(tmp_path, "f.txt", "a\nb\nc\n")
        replacements = [
            Replacement("f.txt", 1, "a", "A", comment="# comment1", action="replace"),
            Replacement("f.txt", 3, "c", "C", comment="# comment3", action="replace"),
        ]
        summary = apply_replacements(replacements, str(tmp_path))

        lines = (tmp_path / "f.txt").read_text().splitlines()
        # Line 3 processed first (reverse order), then line 1
        # After processing line 3: a, b, # comment3, C
        # After processing line 1: # comment1, A, b, # comment3, C
        assert lines == ["# comment1", "A", "b", "# comment3", "C"]
        assert summary.replacements_applied == 2

    def test_comment_inserted_above_replaced_line(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "deploy.yaml", "image: old\n")
        r = Replacement(
            "deploy.yaml", 1, "image: old", "image: new",
            comment="# Replace <AWS_ACCOUNT_ID> with your AWS account ID",
            action="replace",
        )
        summary = apply_replacements([r], str(tmp_path))

        content = (tmp_path / "deploy.yaml").read_text()
        assert content == (
            "# Replace <AWS_ACCOUNT_ID> with your AWS account ID\n"
            "image: new\n"
        )
        assert summary.replacements_applied == 1

    def test_no_comment_when_none(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "old\n")
        r = Replacement("f.txt", 1, "old", "new", comment=None, action="replace")
        apply_replacements([r], str(tmp_path))

        assert (tmp_path / "f.txt").read_text() == "new\n"

    def test_newline_appended_if_missing(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "old\n")
        r = Replacement("f.txt", 1, "old", "new_no_newline", action="replace")
        apply_replacements([r], str(tmp_path))

        assert (tmp_path / "f.txt").read_text() == "new_no_newline\n"

    def test_newline_not_doubled(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "old\n")
        r = Replacement("f.txt", 1, "old", "new_with_newline\n", action="replace")
        apply_replacements([r], str(tmp_path))

        assert (tmp_path / "f.txt").read_text() == "new_with_newline\n"


# ---------------------------------------------------------------------------
# delete_file action
# ---------------------------------------------------------------------------

class TestDeleteFileAction:
    """Tests for the ``delete_file`` action."""

    def test_file_deleted(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "secret.pem", "private key data\n")
        r = Replacement("secret.pem", 1, "", "", action="delete_file")
        summary = apply_replacements([r], str(tmp_path))

        assert not (tmp_path / "secret.pem").exists()
        assert summary.files_deleted == 1

    def test_delete_skips_line_replacements(self, tmp_path: Path) -> None:
        """When delete_file is present, line replacements for that file are skipped."""
        _write_file(tmp_path, "f.txt", "a\nb\n")
        replacements = [
            Replacement("f.txt", 1, "a", "A", action="replace"),
            Replacement("f.txt", 1, "", "", action="delete_file"),
        ]
        summary = apply_replacements(replacements, str(tmp_path))

        assert not (tmp_path / "f.txt").exists()
        assert summary.files_deleted == 1
        assert summary.files_modified == 0

    def test_delete_missing_file_records_error(self, tmp_path: Path) -> None:
        r = Replacement("nonexistent.txt", 1, "", "", action="delete_file")
        summary = apply_replacements([r], str(tmp_path))

        assert summary.files_deleted == 0
        assert len(summary.errors) == 1
        assert "not found" in summary.errors[0].lower()


# ---------------------------------------------------------------------------
# flag_for_review action
# ---------------------------------------------------------------------------

class TestFlagForReviewAction:
    """Tests for the ``flag_for_review`` action."""

    def test_file_not_modified(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "original content\n")
        r = Replacement("f.txt", 1, "original content", "", action="flag_for_review")
        summary = apply_replacements([r], str(tmp_path))

        assert (tmp_path / "f.txt").read_text() == "original content\n"
        assert summary.files_flagged == 1
        assert summary.files_modified == 0

    def test_flag_logged_as_warning(self, tmp_path: Path, caplog) -> None:
        _write_file(tmp_path, "f.txt", "suspicious\n")
        r = Replacement("f.txt", 1, "suspicious", "", action="flag_for_review")
        with caplog.at_level(logging.WARNING):
            apply_replacements([r], str(tmp_path))

        assert any("FLAG FOR REVIEW" in rec.message for rec in caplog.records)


# ---------------------------------------------------------------------------
# Dry-run mode
# ---------------------------------------------------------------------------

class TestDryRun:
    """Tests for dry-run mode."""

    def test_replace_not_written(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "old\n")
        r = Replacement("f.txt", 1, "old", "new", action="replace")
        summary = apply_replacements([r], str(tmp_path), dry_run=True)

        assert (tmp_path / "f.txt").read_text() == "old\n"
        assert summary.replacements_applied == 1
        assert summary.files_modified == 1

    def test_delete_not_performed(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "data\n")
        r = Replacement("f.txt", 1, "", "", action="delete_file")
        summary = apply_replacements([r], str(tmp_path), dry_run=True)

        assert (tmp_path / "f.txt").exists()
        assert summary.files_deleted == 1

    def test_dry_run_logs_replace(self, tmp_path: Path, caplog) -> None:
        _write_file(tmp_path, "f.txt", "old\n")
        r = Replacement("f.txt", 1, "old", "new", action="replace")
        with caplog.at_level(logging.INFO):
            apply_replacements([r], str(tmp_path), dry_run=True)

        assert any("DRY-RUN" in rec.message for rec in caplog.records)

    def test_dry_run_logs_delete(self, tmp_path: Path, caplog) -> None:
        _write_file(tmp_path, "f.txt", "data\n")
        r = Replacement("f.txt", 1, "", "", action="delete_file")
        with caplog.at_level(logging.INFO):
            apply_replacements([r], str(tmp_path), dry_run=True)

        assert any("DRY-RUN" in rec.message and "delete" in rec.message for rec in caplog.records)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Tests for error conditions."""

    def test_line_out_of_range(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "f.txt", "only one line\n")
        r = Replacement("f.txt", 99, "x", "y", action="replace")
        summary = apply_replacements([r], str(tmp_path))

        assert len(summary.errors) == 1
        assert "out of range" in summary.errors[0].lower()

    def test_missing_file_for_replace(self, tmp_path: Path) -> None:
        r = Replacement("missing.txt", 1, "x", "y", action="replace")
        summary = apply_replacements([r], str(tmp_path))

        assert len(summary.errors) == 1
        assert "not found" in summary.errors[0].lower()

    def test_empty_replacements_list(self, tmp_path: Path) -> None:
        summary = apply_replacements([], str(tmp_path))

        assert summary.files_modified == 0
        assert summary.files_deleted == 0
        assert summary.replacements_applied == 0
        assert summary.errors == []


# ---------------------------------------------------------------------------
# Grouping across multiple files
# ---------------------------------------------------------------------------

class TestMultipleFiles:
    """Tests for replacements spanning multiple files."""

    def test_replacements_across_files(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "a.txt", "old_a\n")
        _write_file(tmp_path, "b.txt", "old_b\n")
        replacements = [
            Replacement("a.txt", 1, "old_a", "new_a", action="replace"),
            Replacement("b.txt", 1, "old_b", "new_b", action="replace"),
        ]
        summary = apply_replacements(replacements, str(tmp_path))

        assert (tmp_path / "a.txt").read_text() == "new_a\n"
        assert (tmp_path / "b.txt").read_text() == "new_b\n"
        assert summary.files_modified == 2
        assert summary.replacements_applied == 2

    def test_mixed_actions_across_files(self, tmp_path: Path) -> None:
        _write_file(tmp_path, "keep.txt", "old\n")
        _write_file(tmp_path, "remove.txt", "secret\n")
        _write_file(tmp_path, "review.txt", "suspicious\n")
        replacements = [
            Replacement("keep.txt", 1, "old", "new", action="replace"),
            Replacement("remove.txt", 1, "", "", action="delete_file"),
            Replacement("review.txt", 1, "suspicious", "", action="flag_for_review"),
        ]
        summary = apply_replacements(replacements, str(tmp_path))

        assert (tmp_path / "keep.txt").read_text() == "new\n"
        assert not (tmp_path / "remove.txt").exists()
        assert (tmp_path / "review.txt").read_text() == "suspicious\n"
        assert summary.files_modified == 1
        assert summary.files_deleted == 1
        assert summary.files_flagged == 1


# ---------------------------------------------------------------------------
# Summary dataclass
# ---------------------------------------------------------------------------

class TestApplySummary:
    """Tests for the ApplySummary dataclass defaults."""

    def test_defaults(self) -> None:
        s = ApplySummary()
        assert s.files_modified == 0
        assert s.files_deleted == 0
        assert s.files_flagged == 0
        assert s.replacements_applied == 0
        assert s.errors == []
