import json
import subprocess
from pathlib import Path

import pytest

from tools.quality_gate import QualityGate, is_intentional_secret_fixture


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


@pytest.fixture()
def git_repo(tmp_path: Path) -> Path:
    _run(["git", "init"], tmp_path)
    _run(["git", "config", "user.email", "test@example.com"], tmp_path)
    _run(["git", "config", "user.name", "Test User"], tmp_path)
    return tmp_path


def _commit_all(repo: Path) -> None:
    _run(["git", "add", "-A"], repo)
    _run(["git", "commit", "-m", "test"], repo)


def test_tracked_ignored_files_are_reported(git_repo: Path) -> None:
    (git_repo / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
    ignored_file = git_repo / "node_modules" / "left-pad" / "index.js"
    ignored_file.parent.mkdir(parents=True)
    ignored_file.write_text("module.exports = 1;\n", encoding="utf-8")
    _run(["git", "add", "-f", ".gitignore", "node_modules/left-pad/index.js"], git_repo)
    _run(["git", "commit", "-m", "tracked ignored file"], git_repo)

    findings = QualityGate(git_repo).check_tracked_ignored_files()

    assert findings
    assert findings[0].check == "tracked-ignored"
    assert findings[0].path == Path("node_modules/left-pad/index.js")


def test_deleted_tracked_ignored_files_are_not_reported(git_repo: Path) -> None:
    (git_repo / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
    ignored_file = git_repo / "node_modules" / "left-pad" / "index.js"
    ignored_file.parent.mkdir(parents=True)
    ignored_file.write_text("module.exports = 1;\n", encoding="utf-8")
    _run(["git", "add", "-f", ".gitignore", "node_modules/left-pad/index.js"], git_repo)
    _run(["git", "commit", "-m", "tracked ignored file"], git_repo)
    ignored_file.unlink()

    assert QualityGate(git_repo).check_tracked_ignored_files() == []


def test_project_filter_limits_quality_gate_scope(git_repo: Path) -> None:
    project = git_repo / "project-01-demo"
    project.mkdir()
    project.joinpath("ok.py").write_text("print('ok')\n", encoding="utf-8")
    other = git_repo / "project-02-demo"
    other.mkdir()
    other.joinpath("bad.py").write_text("def nope(:\n", encoding="utf-8")
    _commit_all(git_repo)

    findings = QualityGate(git_repo, project_path="project-01-demo").check_python_syntax()

    assert findings == []


def test_secret_scan_flags_common_patterns_but_skips_intentional_fixtures(
    git_repo: Path,
) -> None:
    real_secret = git_repo / "app.env"
    real_secret.write_text(
        "AWS_SECRET_ACCESS_KEY=abcdefghijklmnopqrstuvwxyz1234567890ABCD\n",
        encoding="utf-8",
    )
    fixture = git_repo / "tools" / "repo_consolidation" / "tests" / "fixture.py"
    fixture.parent.mkdir(parents=True)
    fixture.write_text(
        "TOKEN = 'ghp_abcdefghijklmnopqrstuvwxyz123456789012'\n",
        encoding="utf-8",
    )
    _commit_all(git_repo)

    findings = QualityGate(git_repo).check_secret_patterns()

    assert [finding.path for finding in findings] == [Path("app.env")]
    assert is_intentional_secret_fixture(
        Path("tools/repo_consolidation/tests/fixture.py"),
    )


def test_syntax_checks_report_yaml_shell_and_python_failures(git_repo: Path) -> None:
    (git_repo / "bad.yaml").write_text("items:\n  - ok\n  - : bad\n", encoding="utf-8")
    (git_repo / "bad.sh").write_text("#!/usr/bin/env bash\nif true; then\n", encoding="utf-8")
    (git_repo / "bad.py").write_text("def nope(:\n", encoding="utf-8")
    _commit_all(git_repo)

    findings = QualityGate(git_repo).check_syntax()

    assert {finding.check for finding in findings} == {
        "yaml-syntax",
        "shell-syntax",
        "python-syntax",
    }
    assert {finding.path for finding in findings} == {
        Path("bad.yaml"),
        Path("bad.sh"),
        Path("bad.py"),
    }


def test_package_lock_sanity_reports_bad_json_and_orphan_locks(git_repo: Path) -> None:
    (git_repo / "bad-package-json").mkdir()
    (git_repo / "bad-package-json" / "package.json").write_text("{", encoding="utf-8")
    (git_repo / "orphan-lock").mkdir()
    (git_repo / "orphan-lock" / "package-lock.json").write_text(
        json.dumps({"lockfileVersion": 3}),
        encoding="utf-8",
    )
    _commit_all(git_repo)

    findings = QualityGate(git_repo).check_node_package_locks()

    assert {finding.check for finding in findings} == {"node-package-lock"}
    assert {finding.path for finding in findings} == {
        Path("bad-package-json/package.json"),
        Path("orphan-lock/package-lock.json"),
    }
