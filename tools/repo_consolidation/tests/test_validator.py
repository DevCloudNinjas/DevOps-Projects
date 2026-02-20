"""Tests for the validator module."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.repo_consolidation.models import ValidationReport
from tools.repo_consolidation.validator import count_files_by_extension, validate_fixes


# ---------------------------------------------------------------------------
# count_files_by_extension
# ---------------------------------------------------------------------------


class TestCountFilesByExtension:
    """Tests for the count_files_by_extension helper."""

    def test_counts_by_extension(self, tmp_path: Path) -> None:
        (tmp_path / "readme.md").write_text("# Hello")
        (tmp_path / "notes.md").write_text("# Notes")
        (tmp_path / "main.py").write_text("print('hi')")

        counts = count_files_by_extension(tmp_path)

        assert counts[".md"] == 2
        assert counts[".py"] == 1

    def test_special_filenames(self, tmp_path: Path) -> None:
        (tmp_path / "Jenkinsfile").write_text("pipeline {}")
        (tmp_path / "Dockerfile").write_text("FROM alpine")

        counts = count_files_by_extension(tmp_path)

        assert counts["Jenkinsfile"] == 1
        assert counts["Dockerfile"] == 1

    def test_no_extension_uses_filename(self, tmp_path: Path) -> None:
        (tmp_path / "LICENSE").write_text("MIT")

        counts = count_files_by_extension(tmp_path)

        assert counts["LICENSE"] == 1

    def test_empty_repo(self, tmp_path: Path) -> None:
        counts = count_files_by_extension(tmp_path)

        assert counts == {}

    def test_skips_binary_files(self, tmp_path: Path) -> None:
        (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00")
        (tmp_path / "readme.md").write_text("# Hello")

        counts = count_files_by_extension(tmp_path)

        assert ".png" not in counts
        assert counts[".md"] == 1

    def test_extensions_are_lowercase(self, tmp_path: Path) -> None:
        (tmp_path / "README.MD").write_text("# Hello")
        (tmp_path / "notes.md").write_text("# Notes")

        counts = count_files_by_extension(tmp_path)

        assert counts[".md"] == 2


# ---------------------------------------------------------------------------
# validate_fixes
# ---------------------------------------------------------------------------


class TestValidateFixes:
    """Tests for the validate_fixes function."""

    def test_clean_repo_returns_empty_issues(self, tmp_path: Path) -> None:
        """A repo with no issues should produce zero remaining issues."""
        (tmp_path / "readme.md").write_text("# Clean project\nNo issues here.")

        report = validate_fixes(tmp_path)

        assert isinstance(report, ValidationReport)
        assert report.remaining_issues == []
        assert report.total_files_scanned[".md"] == 1

    def test_detects_remaining_old_url(self, tmp_path: Path) -> None:
        """Old repo URLs should appear in remaining_issues."""
        (tmp_path / "readme.md").write_text(
            "Visit https://github.com/DevCloudNinjas/Zomato-Clone for details."
        )

        report = validate_fixes(tmp_path)

        assert len(report.remaining_issues) == 1
        finding = report.remaining_issues[0]
        assert finding.issue_type == "old_url"
        assert finding.old_repo_name == "Zomato-Clone"

    def test_detects_remaining_credential(self, tmp_path: Path) -> None:
        """PATs should appear in remaining_issues."""
        (tmp_path / "script.sh").write_text(
            "TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789"
        )

        report = validate_fixes(tmp_path)

        assert len(report.remaining_issues) == 1
        assert report.remaining_issues[0].issue_type == "credential"

    def test_detects_remaining_ecr_url(self, tmp_path: Path) -> None:
        """Hardcoded ECR URLs should appear in remaining_issues."""
        (tmp_path / "deploy.yaml").write_text(
            "image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp"
        )

        report = validate_fixes(tmp_path)

        assert len(report.remaining_issues) == 1
        assert report.remaining_issues[0].issue_type == "hardcoded_account_id"

    def test_detects_remaining_docker_image(self, tmp_path: Path) -> None:
        """Stale docker.build calls should appear in remaining_issues."""
        (tmp_path / "Jenkinsfile").write_text(
            'docker.build("devcloudninjas")'
        )

        report = validate_fixes(tmp_path)

        assert any(
            f.issue_type == "stale_docker_image" for f in report.remaining_issues
        )

    def test_multiple_issue_types(self, tmp_path: Path) -> None:
        """Multiple issue types across files should all be captured."""
        (tmp_path / "readme.md").write_text(
            "See https://github.com/DevCloudNinjas/old-repo"
        )
        (tmp_path / "script.sh").write_text(
            "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789"
        )
        (tmp_path / "deploy.yaml").write_text(
            "image: 999888777666.dkr.ecr.eu-west-1.amazonaws.com/app"
        )

        report = validate_fixes(tmp_path)

        issue_types = {f.issue_type for f in report.remaining_issues}
        assert "old_url" in issue_types
        assert "credential" in issue_types
        assert "hardcoded_account_id" in issue_types

    def test_files_scanned_counts_all_extensions(self, tmp_path: Path) -> None:
        """total_files_scanned should reflect all text files found."""
        (tmp_path / "a.md").write_text("clean")
        (tmp_path / "b.yaml").write_text("clean: true")
        (tmp_path / "c.sh").write_text("echo ok")

        report = validate_fixes(tmp_path)

        assert report.total_files_scanned[".md"] == 1
        assert report.total_files_scanned[".yaml"] == 1
        assert report.total_files_scanned[".sh"] == 1

    def test_consolidated_repo_url_not_flagged(self, tmp_path: Path) -> None:
        """URLs pointing to the consolidated repo should not be flagged."""
        (tmp_path / "readme.md").write_text(
            "See https://github.com/DevCloudNinjas/DevOps-Projects for details."
        )

        report = validate_fixes(tmp_path)

        assert report.remaining_issues == []

    def test_returns_validation_report_type(self, tmp_path: Path) -> None:
        """validate_fixes should always return a ValidationReport."""
        report = validate_fixes(tmp_path)

        assert isinstance(report, ValidationReport)
        assert isinstance(report.total_files_scanned, dict)
        assert isinstance(report.remaining_issues, list)
