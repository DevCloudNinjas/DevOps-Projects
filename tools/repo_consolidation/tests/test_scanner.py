"""Tests for scanner.py — file discovery, binary detection, and pattern scanning."""

import os
from pathlib import Path

import pytest

from tools.repo_consolidation.scanner import (
    SCAN_PATTERNS,
    SKIP_DIRS,
    _CONSOLIDATED_REPO_NAME,
    _DOCKER_IMAGE_NAME_PATTERN,
    _DOCKER_IMAGE_PATTERN,
    _ECR_PATTERN,
    _OLD_URL_PATTERN,
    _PAT_PATTERN,
    _PRIVATE_KEY_FILE_PATTERN,
    discover_files,
    is_binary,
    read_text,
    scan_repo,
)


# ---------------------------------------------------------------------------
# is_binary
# ---------------------------------------------------------------------------

def test_is_binary_text_file(tmp_path: Path) -> None:
    f = tmp_path / "hello.txt"
    f.write_text("hello world\n")
    assert is_binary(f) is False


def test_is_binary_with_null_byte(tmp_path: Path) -> None:
    f = tmp_path / "data.bin"
    f.write_bytes(b"some text\x00more bytes")
    assert is_binary(f) is True


def test_is_binary_empty_file(tmp_path: Path) -> None:
    f = tmp_path / "empty"
    f.write_bytes(b"")
    assert is_binary(f) is False


@pytest.mark.skipif(os.name == "nt", reason="chmod does not restrict reads on Windows")
def test_is_binary_unreadable_file(tmp_path: Path) -> None:
    f = tmp_path / "noperm"
    f.write_text("data")
    f.chmod(0o000)
    try:
        # Unreadable files are treated as binary (skipped).
        assert is_binary(f) is True
    finally:
        f.chmod(0o644)


# ---------------------------------------------------------------------------
# read_text
# ---------------------------------------------------------------------------

def test_read_text_utf8(tmp_path: Path) -> None:
    f = tmp_path / "utf8.txt"
    f.write_text("café ☕", encoding="utf-8")
    assert read_text(f) == "café ☕"


def test_read_text_latin1_fallback(tmp_path: Path) -> None:
    f = tmp_path / "latin.txt"
    # \xe9 is 'é' in latin-1 but invalid as a standalone byte in UTF-8.
    f.write_bytes(b"caf\xe9")
    content = read_text(f)
    assert content is not None
    assert "caf" in content


@pytest.mark.skipif(os.name == "nt", reason="chmod does not restrict reads on Windows")
def test_read_text_permission_error(tmp_path: Path) -> None:
    f = tmp_path / "noperm.txt"
    f.write_text("secret")
    f.chmod(0o000)
    try:
        assert read_text(f) is None
    finally:
        f.chmod(0o644)


# ---------------------------------------------------------------------------
# discover_files
# ---------------------------------------------------------------------------

def test_discover_finds_text_files(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("# Hello")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.py").write_text("print(1)")
    found = {p.name for p in discover_files(tmp_path)}
    assert found == {"a.md", "b.py"}


def test_discover_skips_binary_files(tmp_path: Path) -> None:
    (tmp_path / "text.txt").write_text("ok")
    (tmp_path / "img.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00")
    found = {p.name for p in discover_files(tmp_path)}
    assert found == {"text.txt"}


@pytest.mark.parametrize("dirname", sorted(SKIP_DIRS))
def test_discover_skips_special_dirs(tmp_path: Path, dirname: str) -> None:
    skip = tmp_path / dirname
    skip.mkdir()
    (skip / "file.txt").write_text("should be skipped")
    (tmp_path / "keep.txt").write_text("keep")
    found = {p.name for p in discover_files(tmp_path)}
    assert found == {"keep.txt"}


@pytest.mark.skipif(os.name == "nt", reason="Symlinks require elevated privileges on Windows")
def test_discover_handles_symlink_loop(tmp_path: Path) -> None:
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "file.txt").write_text("data")
    link = sub / "loop"
    link.symlink_to(sub)
    # Should not hang or crash.
    found = list(discover_files(tmp_path))
    names = {p.name for p in found}
    assert "file.txt" in names


@pytest.mark.skipif(os.name == "nt", reason="chmod does not restrict dir access on Windows")
def test_discover_handles_permission_error_on_dir(tmp_path: Path) -> None:
    secret = tmp_path / "secret"
    secret.mkdir()
    (secret / "file.txt").write_text("hidden")
    secret.chmod(0o000)
    (tmp_path / "visible.txt").write_text("ok")
    try:
        found = {p.name for p in discover_files(tmp_path)}
        # visible.txt should still be found; secret dir is inaccessible.
        assert "visible.txt" in found
    finally:
        secret.chmod(0o755)


def test_discover_empty_repo(tmp_path: Path) -> None:
    assert list(discover_files(tmp_path)) == []


def test_discover_nested_skip_dirs(tmp_path: Path) -> None:
    """Skip dirs should be pruned at any depth."""
    deep = tmp_path / "a" / "b" / "node_modules"
    deep.mkdir(parents=True)
    (deep / "pkg.json").write_text("{}")
    (tmp_path / "a" / "b" / "code.js").write_text("var x = 1;")
    found = {p.name for p in discover_files(tmp_path)}
    assert found == {"code.js"}


# ===========================================================================
# Pattern unit tests
# ===========================================================================


class TestOldUrlPattern:
    """Tests for _OLD_URL_PATTERN."""

    def test_matches_camelcase_org(self) -> None:
        m = _OLD_URL_PATTERN.search("github.com/DevCloudNinjas/Zomato-Clone")
        assert m is not None
        assert m.group(2) == "Zomato-Clone"

    def test_matches_lowercase_org(self) -> None:
        m = _OLD_URL_PATTERN.search("github.com/devcloudninjas/devops-bootcamp")
        assert m is not None
        assert m.group(2) == "devops-bootcamp"

    def test_case_insensitive_org(self) -> None:
        m = _OLD_URL_PATTERN.search("github.com/DEVCLOUDNINJAS/SomeRepo")
        assert m is not None

    def test_in_markdown_link(self) -> None:
        line = "[Clone](https://github.com/DevCloudNinjas/Zomato-Clone)"
        m = _OLD_URL_PATTERN.search(line)
        assert m is not None
        assert m.group(2) == "Zomato-Clone"

    def test_in_go_import(self) -> None:
        line = '"github.com/devcloudninjas/devops-bootcamp/pkg/util"'
        m = _OLD_URL_PATTERN.search(line)
        assert m is not None
        assert m.group(2) == "devops-bootcamp"

    def test_in_json_string(self) -> None:
        line = '  "repository": "https://github.com/devcloudninjas/devops-bootcamp"'
        m = _OLD_URL_PATTERN.search(line)
        assert m is not None

    def test_in_yaml_value(self) -> None:
        line = "url: https://github.com/DevCloudNinjas/full-stack-blogging-app"
        m = _OLD_URL_PATTERN.search(line)
        assert m is not None
        assert m.group(2) == "full-stack-blogging-app"

    def test_in_shell_variable(self) -> None:
        line = 'REPO_URL="https://github.com/DevCloudNinjas/Zomato-Clone.git"'
        m = _OLD_URL_PATTERN.search(line)
        assert m is not None

    def test_no_match_on_unrelated_url(self) -> None:
        assert _OLD_URL_PATTERN.search("github.com/someoneelse/repo") is None


class TestPatPattern:
    """Tests for _PAT_PATTERN."""

    def test_matches_valid_pat(self) -> None:
        pat = "ghp_" + "A" * 36
        assert _PAT_PATTERN.search(pat) is not None

    def test_no_match_short_pat(self) -> None:
        pat = "ghp_" + "A" * 35
        assert _PAT_PATTERN.search(pat) is None

    def test_matches_in_shell_context(self) -> None:
        line = f'TOKEN="ghp_{"a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"}"; echo $TOKEN'
        assert _PAT_PATTERN.search(line) is not None


class TestEcrPattern:
    """Tests for _ECR_PATTERN."""

    def test_matches_ecr_url(self) -> None:
        url = "221650130255.dkr.ecr.us-west-2.amazonaws.com"
        assert _ECR_PATTERN.search(url) is not None

    def test_matches_different_region(self) -> None:
        url = "123456789012.dkr.ecr.eu-central-1.amazonaws.com"
        assert _ECR_PATTERN.search(url) is not None

    def test_no_match_short_account_id(self) -> None:
        url = "12345.dkr.ecr.us-east-1.amazonaws.com"
        assert _ECR_PATTERN.search(url) is None


class TestDockerImagePattern:
    """Tests for _DOCKER_IMAGE_PATTERN."""

    def test_matches_docker_build_double_quotes(self) -> None:
        line = 'docker.build("devcloudninjas")'
        assert _DOCKER_IMAGE_PATTERN.search(line) is not None

    def test_matches_docker_build_single_quotes(self) -> None:
        line = "docker.build('devcloudninjas')"
        assert _DOCKER_IMAGE_PATTERN.search(line) is not None

    def test_case_insensitive(self) -> None:
        line = 'docker.build("DevCloudNinjas")'
        assert _DOCKER_IMAGE_PATTERN.search(line) is not None


class TestDockerImageNamePattern:
    """Tests for _DOCKER_IMAGE_NAME_PATTERN (standalone image name)."""

    def test_matches_standalone_name(self) -> None:
        line = "image: devcloudninjas"
        assert _DOCKER_IMAGE_NAME_PATTERN.search(line) is not None

    def test_no_match_inside_url(self) -> None:
        # The pattern uses negative lookbehind/ahead for word/slash chars,
        # so it correctly does NOT match when embedded in a URL path.
        line = "github.com/devcloudninjas/repo"
        assert _DOCKER_IMAGE_NAME_PATTERN.search(line) is None


class TestPrivateKeyFilePattern:
    """Tests for _PRIVATE_KEY_FILE_PATTERN."""

    def test_matches_ppk(self) -> None:
        assert _PRIVATE_KEY_FILE_PATTERN.search("mykey.ppk") is not None

    def test_matches_pem(self) -> None:
        assert _PRIVATE_KEY_FILE_PATTERN.search("server.pem") is not None

    def test_case_insensitive(self) -> None:
        assert _PRIVATE_KEY_FILE_PATTERN.search("KEY.PEM") is not None

    def test_no_match_other_ext(self) -> None:
        assert _PRIVATE_KEY_FILE_PATTERN.search("file.txt") is None


# ===========================================================================
# scan_repo integration tests
# ===========================================================================


class TestScanRepo:
    """Integration tests for scan_repo."""

    def test_detects_old_url_in_markdown(self, tmp_path: Path) -> None:
        md = tmp_path / "README.md"
        md.write_text("See [Zomato](https://github.com/DevCloudNinjas/Zomato-Clone)\n")
        findings = scan_repo(tmp_path)
        old_url_findings = [f for f in findings if f.issue_type == "old_url"]
        assert len(old_url_findings) == 1
        assert old_url_findings[0].old_repo_name == "Zomato-Clone"
        assert old_url_findings[0].line_number == 1
        assert old_url_findings[0].file_type == ".md"

    def test_detects_pat_in_shell_script(self, tmp_path: Path) -> None:
        sh = tmp_path / "deploy.sh"
        pat = "ghp_" + "x" * 36
        sh.write_text(f'TOKEN="{pat}"\n')
        findings = scan_repo(tmp_path)
        cred_findings = [f for f in findings if f.issue_type == "credential"]
        assert len(cred_findings) == 1
        assert cred_findings[0].matched_text == pat

    def test_detects_ecr_url(self, tmp_path: Path) -> None:
        yml = tmp_path / "deployment.yaml"
        yml.write_text("image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/myapp\n")
        findings = scan_repo(tmp_path)
        ecr_findings = [f for f in findings if f.issue_type == "hardcoded_account_id"]
        assert len(ecr_findings) == 1

    def test_detects_docker_build(self, tmp_path: Path) -> None:
        jf = tmp_path / "Jenkinsfile"
        jf.write_text('docker.build("devcloudninjas")\n')
        findings = scan_repo(tmp_path)
        docker_findings = [f for f in findings if f.issue_type == "stale_docker_image"]
        assert len(docker_findings) == 1

    def test_detects_standalone_docker_image_name(self, tmp_path: Path) -> None:
        yml = tmp_path / "deploy.yaml"
        yml.write_text("image: devcloudninjas\n")
        findings = scan_repo(tmp_path)
        docker_findings = [f for f in findings if f.issue_type == "stale_docker_image"]
        assert len(docker_findings) == 1

    def test_detects_private_key_file(self, tmp_path: Path) -> None:
        pem = tmp_path / "server.pem"
        pem.write_text("-----BEGIN RSA PRIVATE KEY-----\ndata\n")
        findings = scan_repo(tmp_path)
        cred_findings = [f for f in findings if f.issue_type == "credential"]
        assert any("server.pem" in f.matched_text for f in cred_findings)

    def test_skips_consolidated_repo_url(self, tmp_path: Path) -> None:
        md = tmp_path / "README.md"
        md.write_text("See https://github.com/DevCloudNinjas/DevOps-Projects\n")
        findings = scan_repo(tmp_path)
        old_url_findings = [f for f in findings if f.issue_type == "old_url"]
        assert len(old_url_findings) == 0

    def test_file_path_is_relative(self, tmp_path: Path) -> None:
        sub = tmp_path / "project-13"
        sub.mkdir()
        md = sub / "README.md"
        md.write_text("https://github.com/DevCloudNinjas/Zomato-Clone\n")
        findings = scan_repo(tmp_path)
        assert findings[0].file_path == os.path.join("project-13", "README.md")

    def test_multiple_patterns_same_file(self, tmp_path: Path) -> None:
        sh = tmp_path / "setup.sh"
        pat = "ghp_" + "A" * 36
        sh.write_text(
            f'REPO="https://github.com/DevCloudNinjas/Zomato-Clone"\n'
            f'TOKEN="{pat}"\n'
        )
        findings = scan_repo(tmp_path)
        types = {f.issue_type for f in findings}
        assert "old_url" in types
        assert "credential" in types

    def test_go_import_detection(self, tmp_path: Path) -> None:
        go = tmp_path / "main.go"
        go.write_text(
            'package main\n\n'
            'import "github.com/devcloudninjas/devops-bootcamp/pkg/util"\n'
        )
        findings = scan_repo(tmp_path)
        old_url_findings = [f for f in findings if f.issue_type == "old_url"]
        assert len(old_url_findings) == 1
        assert old_url_findings[0].old_repo_name == "devops-bootcamp"

    def test_json_string_detection(self, tmp_path: Path) -> None:
        pkg = tmp_path / "package.json"
        pkg.write_text(
            '{\n'
            '  "repository": "https://github.com/devcloudninjas/devops-bootcamp"\n'
            '}\n'
        )
        findings = scan_repo(tmp_path)
        old_url_findings = [f for f in findings if f.issue_type == "old_url"]
        assert len(old_url_findings) == 1

    def test_yaml_value_detection(self, tmp_path: Path) -> None:
        yml = tmp_path / "config.yaml"
        yml.write_text("repo: https://github.com/DevCloudNinjas/full-stack-blogging-app\n")
        findings = scan_repo(tmp_path)
        old_url_findings = [f for f in findings if f.issue_type == "old_url"]
        assert len(old_url_findings) == 1

    def test_empty_repo_returns_no_findings(self, tmp_path: Path) -> None:
        assert scan_repo(tmp_path) == []

    def test_no_false_positive_on_clean_file(self, tmp_path: Path) -> None:
        md = tmp_path / "clean.md"
        md.write_text("# Hello World\n\nThis is a clean file with no issues.\n")
        assert scan_repo(tmp_path) == []

    def test_multiple_matches_on_same_line(self, tmp_path: Path) -> None:
        md = tmp_path / "links.md"
        md.write_text(
            "[A](https://github.com/DevCloudNinjas/Zomato-Clone) "
            "[B](https://github.com/DevCloudNinjas/full-stack-blogging-app)\n"
        )
        findings = scan_repo(tmp_path)
        old_url_findings = [f for f in findings if f.issue_type == "old_url"]
        assert len(old_url_findings) == 2
        names = {f.old_repo_name for f in old_url_findings}
        assert names == {"Zomato-Clone", "full-stack-blogging-app"}

    def test_custom_patterns(self, tmp_path: Path) -> None:
        """scan_repo accepts custom pattern dict."""
        import re

        txt = tmp_path / "data.txt"
        txt.write_text("CUSTOM_MATCH_HERE\n")
        custom = {"custom_type": re.compile(r"CUSTOM_MATCH_HERE")}
        findings = scan_repo(tmp_path, patterns=custom)
        assert len(findings) == 1
        assert findings[0].issue_type == "custom_type"
