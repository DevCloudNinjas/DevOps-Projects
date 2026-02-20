"""Tests for the report generator module."""

from __future__ import annotations

from tools.repo_consolidation.models import Finding, ValidationReport
from tools.repo_consolidation.report import (
    generate_report,
    generate_unresolved_report,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_finding(
    file_path: str = "readme.md",
    line_number: int = 1,
    matched_text: str = "https://github.com/DevCloudNinjas/old-repo",
    issue_type: str = "old_url",
    old_repo_name: str = "old-repo",
    context: str = "See https://github.com/DevCloudNinjas/old-repo",
    file_type: str = ".md",
) -> Finding:
    return Finding(
        file_path=file_path,
        line_number=line_number,
        matched_text=matched_text,
        issue_type=issue_type,
        old_repo_name=old_repo_name,
        context=context,
        file_type=file_type,
    )


def _make_validation(
    total_files_scanned: dict[str, int] | None = None,
    total_references_fixed: int = 0,
    total_credentials_removed: int = 0,
    total_account_ids_parameterized: int = 0,
    total_links_validated: int = 0,
    total_broken_relative_paths: int = 0,
    remaining_issues: list[Finding] | None = None,
) -> ValidationReport:
    return ValidationReport(
        total_files_scanned=total_files_scanned or {},
        total_references_fixed=total_references_fixed,
        total_credentials_removed=total_credentials_removed,
        total_account_ids_parameterized=total_account_ids_parameterized,
        total_links_validated=total_links_validated,
        total_broken_relative_paths=total_broken_relative_paths,
        remaining_issues=remaining_issues or [],
    )


# ---------------------------------------------------------------------------
# generate_report
# ---------------------------------------------------------------------------


class TestGenerateReport:
    """Tests for the generate_report function."""

    def test_contains_header(self) -> None:
        report = generate_report([], _make_validation())
        assert "Repo Consolidation" in report
        assert "Remediation Report" in report

    def test_files_scanned_by_type(self) -> None:
        validation = _make_validation(
            total_files_scanned={".md": 10, ".yaml": 5, ".py": 3},
        )
        report = generate_report([], validation)

        assert ".md: 10" in report
        assert ".yaml: 5" in report
        assert ".py: 3" in report

    def test_files_scanned_empty(self) -> None:
        report = generate_report([], _make_validation())
        assert "(none)" in report

    def test_initial_scan_summary(self) -> None:
        findings = [
            _make_finding(issue_type="old_url"),
            _make_finding(issue_type="old_url"),
            _make_finding(issue_type="credential"),
        ]
        report = generate_report(findings, _make_validation())

        assert "Total issues found: 3" in report
        assert "old_url: 2" in report
        assert "credential: 1" in report

    def test_fix_summary_values(self) -> None:
        validation = _make_validation(
            total_references_fixed=15,
            total_credentials_removed=4,
            total_account_ids_parameterized=6,
        )
        report = generate_report([], validation)

        assert "References fixed:        15" in report
        assert "Credentials removed:     4" in report
        assert "Account IDs parameterized: 6" in report

    def test_validation_results(self) -> None:
        validation = _make_validation(
            total_links_validated=20,
            total_broken_relative_paths=2,
            remaining_issues=[_make_finding()],
        )
        report = generate_report([], validation)

        assert "Links validated:         20" in report
        assert "Broken relative paths:   2" in report
        assert "Remaining issues:        1" in report

    def test_no_remaining_issues_omits_detail(self) -> None:
        report = generate_report([], _make_validation())
        assert "Unresolved Issues" not in report

    def test_remaining_issues_included(self) -> None:
        issue = _make_finding(
            file_path="project-13/README.md",
            line_number=42,
            issue_type="old_url",
            matched_text="https://github.com/DevCloudNinjas/Zomato-Clone",
        )
        validation = _make_validation(remaining_issues=[issue])
        report = generate_report([], validation)

        assert "Unresolved Issues" in report
        assert "project-13/README.md" in report
        assert "Line 42" in report
        assert "old_url" in report

    def test_returns_string(self) -> None:
        report = generate_report([], _make_validation())
        assert isinstance(report, str)

    def test_multiple_issue_types_in_scan(self) -> None:
        findings = [
            _make_finding(issue_type="old_url"),
            _make_finding(issue_type="credential"),
            _make_finding(issue_type="hardcoded_account_id"),
            _make_finding(issue_type="stale_docker_image"),
        ]
        report = generate_report(findings, _make_validation())

        assert "Total issues found: 4" in report
        assert "old_url: 1" in report
        assert "credential: 1" in report
        assert "hardcoded_account_id: 1" in report
        assert "stale_docker_image: 1" in report


# ---------------------------------------------------------------------------
# generate_unresolved_report
# ---------------------------------------------------------------------------


class TestGenerateUnresolvedReport:
    """Tests for the generate_unresolved_report function."""

    def test_no_issues_returns_short_message(self) -> None:
        result = generate_unresolved_report(_make_validation())
        assert result == "No unresolved issues."

    def test_contains_header(self) -> None:
        validation = _make_validation(remaining_issues=[_make_finding()])
        result = generate_unresolved_report(validation)
        assert "Unresolved Issues Report" in result

    def test_lists_file_path_and_line(self) -> None:
        issue = _make_finding(
            file_path="src/main.go",
            line_number=17,
            matched_text="github.com/devcloudninjas/old",
            issue_type="old_url",
        )
        result = generate_unresolved_report(_make_validation(remaining_issues=[issue]))

        assert "src/main.go" in result
        assert "Line 17" in result
        assert "old_url" in result

    def test_groups_by_file(self) -> None:
        issues = [
            _make_finding(file_path="a.md", line_number=1),
            _make_finding(file_path="a.md", line_number=5),
            _make_finding(file_path="b.yaml", line_number=3),
        ]
        result = generate_unresolved_report(
            _make_validation(remaining_issues=issues),
        )

        # Both files should appear
        assert "a.md" in result
        assert "b.yaml" in result

    def test_issues_sorted_by_line_within_file(self) -> None:
        issues = [
            _make_finding(file_path="a.md", line_number=10, matched_text="url10"),
            _make_finding(file_path="a.md", line_number=2, matched_text="url2"),
        ]
        result = generate_unresolved_report(
            _make_validation(remaining_issues=issues),
        )

        pos_2 = result.index("Line 2")
        pos_10 = result.index("Line 10")
        assert pos_2 < pos_10

    def test_returns_string(self) -> None:
        result = generate_unresolved_report(_make_validation())
        assert isinstance(result, str)
