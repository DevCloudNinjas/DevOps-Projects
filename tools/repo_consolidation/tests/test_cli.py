"""Tests for the CLI pipeline integration (task 10.1).

Validates that the main() function correctly wires all pipeline stages
together: scan → classify → fix → apply → validate → report.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.repo_consolidation.cli import main


@pytest.fixture()
def mini_repo(tmp_path: Path) -> Path:
    """Create a minimal repo with a known old URL for end-to-end testing."""
    readme = tmp_path / "README.md"
    readme.write_text(
        "# Project\n"
        "See https://github.com/DevCloudNinjas/Zomato-Clone for details.\n",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture()
def empty_repo(tmp_path: Path) -> Path:
    """Create an empty repo directory."""
    return tmp_path


class TestMainReturnCodes:
    """Verify main() returns correct exit codes."""

    def test_nonexistent_repo_returns_1(self, tmp_path: Path) -> None:
        bad_path = str(tmp_path / "does_not_exist")
        assert main([bad_path]) == 1

    def test_empty_repo_returns_0(self, empty_repo: Path) -> None:
        result = main([str(empty_repo)])
        assert result == 0

    def test_dry_run_does_not_modify_files(self, mini_repo: Path) -> None:
        readme = mini_repo / "README.md"
        original = readme.read_text(encoding="utf-8")

        main([str(mini_repo), "--dry-run"])

        assert readme.read_text(encoding="utf-8") == original


class TestMainPipelineStages:
    """Verify that main() calls all pipeline stages in order."""

    def test_scan_is_called(self, empty_repo: Path) -> None:
        with patch("tools.repo_consolidation.cli.scan_repo", return_value=[]) as mock_scan:
            main([str(empty_repo)])
            mock_scan.assert_called_once()

    def test_validate_is_called(self, empty_repo: Path) -> None:
        with patch("tools.repo_consolidation.cli.validate_fixes") as mock_val:
            from tools.repo_consolidation.models import ValidationReport
            mock_val.return_value = ValidationReport()
            main([str(empty_repo)])
            mock_val.assert_called_once()

    def test_generate_report_is_called(self, empty_repo: Path) -> None:
        with patch("tools.repo_consolidation.cli.generate_report", return_value="report") as mock_rpt:
            main([str(empty_repo)])
            mock_rpt.assert_called_once()


class TestReportOutput:
    """Verify --report-output writes the report to a file."""

    def test_report_written_to_file(self, empty_repo: Path, tmp_path: Path) -> None:
        report_file = tmp_path / "output" / "report.txt"
        main([str(empty_repo), "--report-output", str(report_file)])

        assert report_file.exists()
        content = report_file.read_text(encoding="utf-8")
        assert "Remediation Report" in content

    def test_report_printed_to_stdout(self, empty_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
        main([str(empty_repo)])
        captured = capsys.readouterr()
        assert "Remediation Report" in captured.out


class TestVerboseFlag:
    """Verify --verbose enables debug logging."""

    def test_verbose_sets_debug_level(self, empty_repo: Path) -> None:
        import logging
        with patch("tools.repo_consolidation.cli.configure_logging") as mock_cfg:
            main([str(empty_repo), "--verbose"])
            mock_cfg.assert_called_once_with(True)


class TestErrorHandling:
    """Verify graceful error handling on individual file failures."""

    def test_fixer_exception_is_caught(self, mini_repo: Path) -> None:
        """If a fixer raises, the pipeline should log and continue."""
        with patch(
            "tools.repo_consolidation.cli.fix_old_url",
            side_effect=RuntimeError("boom"),
        ):
            # Should not raise — errors are caught per-finding
            result = main([str(mini_repo), "--dry-run"])
            # Pipeline completes (may return 0 or 1 depending on validation)
            assert result in (0, 1)

    def test_scan_exception_returns_1(self, empty_repo: Path) -> None:
        with patch(
            "tools.repo_consolidation.cli.scan_repo",
            side_effect=RuntimeError("scan failed"),
        ):
            assert main([str(empty_repo)]) == 1
