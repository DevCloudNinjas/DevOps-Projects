"""Unit tests for the old-URL fixer in fixers.py."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from tools.repo_consolidation.fixers import fix_account_id, fix_docker_image, fix_old_url
from tools.repo_consolidation.models import Finding


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_finding(
    file_path: str = "project-13-zomato-clone-devsecops/README.md",
    line_number: int = 10,
    matched_text: str = "github.com/DevCloudNinjas/Zomato-Clone",
    issue_type: str = "old_url",
    old_repo_name: str = "Zomato-Clone",
    context: str = "See https://github.com/DevCloudNinjas/Zomato-Clone for details",
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


# ---------------------------------------------------------------------------
# Tests: basic behaviour
# ---------------------------------------------------------------------------

class TestFixOldUrlBasic:
    """Core behaviour of fix_old_url."""

    def test_returns_none_for_unmapped_repo(self):
        finding = _make_finding(old_repo_name="nonexistent-repo-xyz")
        result = fix_old_url(finding)
        assert result is None

    def test_returns_none_for_empty_repo_name(self):
        finding = _make_finding(old_repo_name="")
        result = fix_old_url(finding)
        assert result is None

    def test_returns_replacement_with_correct_file_path(self):
        finding = _make_finding()
        result = fix_old_url(finding)
        assert result is not None
        assert result.file_path == finding.file_path

    def test_returns_replacement_with_correct_line_number(self):
        finding = _make_finding()
        result = fix_old_url(finding)
        assert result is not None
        assert result.line_number == finding.line_number

    def test_old_text_is_context_line(self):
        finding = _make_finding()
        result = fix_old_url(finding)
        assert result is not None
        assert result.old_text == finding.context

    def test_action_is_replace(self):
        finding = _make_finding()
        result = fix_old_url(finding)
        assert result is not None
        assert result.action == "replace"


# ---------------------------------------------------------------------------
# Tests: markdown links
# ---------------------------------------------------------------------------

class TestFixOldUrlMarkdownLinks:
    """Markdown link [text](url) replacement."""

    def test_markdown_link_becomes_relative_path(self):
        context = "[Zomato Clone](https://github.com/DevCloudNinjas/Zomato-Clone)"
        finding = _make_finding(
            file_path="project-32-tetris-devsecops-k8s/README.md",
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "[Zomato Clone](../project-13-zomato-clone-devsecops)" in result.new_text

    def test_markdown_link_with_subpath(self):
        context = "[Setup](https://github.com/DevCloudNinjas/Zomato-Clone/blob/main/docs/setup.md)"
        finding = _make_finding(
            file_path="project-32-tetris-devsecops-k8s/README.md",
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "../project-13-zomato-clone-devsecops/docs/setup.md" in result.new_text

    def test_markdown_link_preserves_link_text(self):
        context = "[My Custom Text](https://github.com/DevCloudNinjas/Zomato-Clone)"
        finding = _make_finding(
            file_path="README.md",
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "[My Custom Text](" in result.new_text

    def test_markdown_link_same_directory(self):
        context = "[Clone](https://github.com/DevCloudNinjas/Zomato-Clone)"
        finding = _make_finding(
            file_path="project-13-zomato-clone-devsecops/README.md",
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        # Same directory → should be just "."
        assert "[Clone](.)" in result.new_text


# ---------------------------------------------------------------------------
# Tests: git clone URLs
# ---------------------------------------------------------------------------

class TestFixOldUrlClone:
    """Git clone URL replacement."""

    def test_git_clone_url_replaced(self):
        context = "git clone https://github.com/DevCloudNinjas/Zomato-Clone.git"
        finding = _make_finding(
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "https://github.com/DevCloudNinjas/DevOps-Projects.git" in result.new_text

    def test_git_clone_without_dot_git(self):
        context = "git clone https://github.com/DevCloudNinjas/Zomato-Clone"
        finding = _make_finding(
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "DevOps-Projects" in result.new_text


# ---------------------------------------------------------------------------
# Tests: Go import paths
# ---------------------------------------------------------------------------

class TestFixOldUrlGoImports:
    """Go import path replacement."""

    def test_go_import_path_updated(self):
        context = '"github.com/devcloudninjas/devops-bootcamp/pkg/util"'
        finding = _make_finding(
            file_path="learning/devops-bootcamp/examples/codeQuality/goExamples/example_test.go",
            context=context,
            old_repo_name="devops-bootcamp",
            file_type=".go",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp/pkg/util" in result.new_text

    def test_go_import_no_subpath(self):
        context = '"github.com/devcloudninjas/devops-bootcamp"'
        finding = _make_finding(
            file_path="learning/devops-bootcamp/go.mod",
            context=context,
            old_repo_name="devops-bootcamp",
            file_type=".mod",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp" in result.new_text


# ---------------------------------------------------------------------------
# Tests: JSON metadata fields
# ---------------------------------------------------------------------------

class TestFixOldUrlJsonMetadata:
    """JSON metadata field (repository, bugs, homepage) replacement."""

    def test_package_json_repository_url(self):
        context = '  "repository": "https://github.com/devcloudninjas/devops-bootcamp",'
        finding = _make_finding(
            file_path="learning/devops-bootcamp/package.json",
            context=context,
            old_repo_name="devops-bootcamp",
            file_type=".json",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "DevOps-Projects/tree/main/learning/devops-bootcamp" in result.new_text

    def test_package_json_bugs_url(self):
        context = '  "bugs": { "url": "https://github.com/devcloudninjas/devops-bootcamp/issues" },'
        finding = _make_finding(
            file_path="learning/devops-bootcamp/package.json",
            context=context,
            old_repo_name="devops-bootcamp",
            file_type=".json",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "DevOps-Projects/tree/main/learning/devops-bootcamp" in result.new_text

    def test_package_json_homepage_url(self):
        context = '  "homepage": "https://github.com/devcloudninjas/devops-bootcamp#readme",'
        finding = _make_finding(
            file_path="learning/devops-bootcamp/package.json",
            context=context,
            old_repo_name="devops-bootcamp",
            file_type=".json",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "DevOps-Projects/tree/main/learning/devops-bootcamp" in result.new_text


# ---------------------------------------------------------------------------
# Tests: raw URLs in comments / documentation
# ---------------------------------------------------------------------------

class TestFixOldUrlRawUrls:
    """Raw URLs in comments, docs, and string literals."""

    def test_raw_url_in_comment(self):
        context = "# See https://github.com/DevCloudNinjas/Zomato-Clone for reference"
        finding = _make_finding(
            file_path="project-13-zomato-clone-devsecops/deploy.sh",
            context=context,
            old_repo_name="Zomato-Clone",
            file_type=".sh",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "DevOps-Projects/tree/main/project-13-zomato-clone-devsecops" in result.new_text
        assert "Zomato-Clone" not in result.new_text

    def test_raw_url_with_subpath(self):
        context = "# Ref: https://github.com/DevCloudNinjas/Zomato-Clone/tree/main/docs"
        finding = _make_finding(
            file_path="project-13-zomato-clone-devsecops/deploy.sh",
            context=context,
            old_repo_name="Zomato-Clone",
            file_type=".sh",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "Zomato-Clone" not in result.new_text


# ---------------------------------------------------------------------------
# Tests: unverified target path
# ---------------------------------------------------------------------------

class TestFixOldUrlTargetVerification:
    """Target path existence verification."""

    def test_unverified_comment_when_target_missing(self):
        finding = _make_finding(
            context="See https://github.com/DevCloudNinjas/Zomato-Clone for details",
            old_repo_name="Zomato-Clone",
        )
        # Use a repo_root that definitely doesn't contain the target.
        with tempfile.TemporaryDirectory() as tmpdir:
            result = fix_old_url(finding, repo_root=tmpdir)
        assert result is not None
        assert result.comment is not None
        assert "could not be verified" in result.comment

    def test_no_unverified_comment_when_target_exists(self):
        finding = _make_finding(
            context="See https://github.com/DevCloudNinjas/Zomato-Clone for details",
            old_repo_name="Zomato-Clone",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create the target directory.
            target = Path(tmpdir) / "project-13-zomato-clone-devsecops"
            target.mkdir()
            result = fix_old_url(finding, repo_root=tmpdir)
        assert result is not None
        assert result.comment is None


# ---------------------------------------------------------------------------
# Tests: case-insensitive org matching
# ---------------------------------------------------------------------------

class TestFixOldUrlCaseInsensitive:
    """Case-insensitive org name matching."""

    def test_lowercase_org(self):
        context = "See https://github.com/devcloudninjas/Zomato-Clone for details"
        finding = _make_finding(
            context=context,
            old_repo_name="Zomato-Clone",
        )
        result = fix_old_url(finding)
        assert result is not None
        assert "Zomato-Clone" not in result.new_text or "project-13" in result.new_text


# ---------------------------------------------------------------------------
# Tests: credential fixer
# ---------------------------------------------------------------------------

from tools.repo_consolidation.fixers import fix_credential


def _make_credential_finding(
    file_path: str = "project-47-django-saas-ecommerce/autoPush.sh",
    line_number: int = 5,
    matched_text: str = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij",
    issue_type: str = "credential",
    old_repo_name: str = "",
    context: str = 'TOKEN="ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij"',
    file_type: str = ".sh",
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


class TestFixCredentialShellPAT:
    """PAT replacement in shell scripts."""

    def test_pat_replaced_with_github_token(self):
        finding = _make_credential_finding()
        result = fix_credential(finding)
        assert result.action == "replace"
        assert "$GITHUB_TOKEN" in result.new_text
        assert "ghp_" not in result.new_text

    def test_pat_comment_added(self):
        finding = _make_credential_finding()
        result = fix_credential(finding)
        assert result.comment == "# Set GITHUB_TOKEN environment variable"

    def test_pat_preserves_surrounding_text(self):
        context = 'git push https://ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij@github.com/repo'
        finding = _make_credential_finding(context=context)
        result = fix_credential(finding)
        assert "git push" in result.new_text
        assert "$GITHUB_TOKEN" in result.new_text

    def test_file_path_preserved(self):
        finding = _make_credential_finding()
        result = fix_credential(finding)
        assert result.file_path == finding.file_path
        assert result.line_number == finding.line_number


class TestFixCredentialYAMLPAT:
    """PAT replacement in YAML workflow files."""

    def test_yaml_pat_replaced_with_secrets(self):
        finding = _make_credential_finding(
            file_path="project-47/.github/workflows/SonarQube-workflow.yaml",
            context="  token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij",
            file_type=".yaml",
        )
        result = fix_credential(finding)
        assert result.action == "replace"
        assert "${{ secrets.GITHUB_TOKEN }}" in result.new_text
        assert "ghp_" not in result.new_text

    def test_yaml_comment_added(self):
        finding = _make_credential_finding(
            file_path="project-47/.github/workflows/SonarQube-workflow.yaml",
            context="  token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij",
            file_type=".yaml",
        )
        result = fix_credential(finding)
        assert result.comment is not None
        assert "secret" in result.comment.lower() or "GitHub Actions" in result.comment

    def test_yml_extension_also_works(self):
        finding = _make_credential_finding(
            file_path="project-47/.github/workflows/deploy.yml",
            context="  token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij",
            file_type=".yml",
        )
        result = fix_credential(finding)
        assert "${{ secrets.GITHUB_TOKEN }}" in result.new_text


class TestFixCredentialPrivateKeyFiles:
    """Private key file (.ppk, .pem) flagging."""

    def test_ppk_file_flagged_for_review(self):
        finding = _make_credential_finding(
            file_path="project-35-devsecops-pipeline-series/step-1-infra-creation/key.ppk",
            matched_text="key.ppk",
            context="Private key file: key.ppk",
            file_type=".ppk",
        )
        result = fix_credential(finding)
        assert result.action == "flag_for_review"

    def test_pem_file_flagged_for_review(self):
        finding = _make_credential_finding(
            file_path="project-35-devsecops-pipeline-series/step-1-infra-creation/server.pem",
            matched_text="server.pem",
            context="Private key file: server.pem",
            file_type=".pem",
        )
        result = fix_credential(finding)
        assert result.action == "flag_for_review"

    def test_private_key_comment_mentions_removal(self):
        finding = _make_credential_finding(
            file_path="project-35/key.ppk",
            matched_text="key.ppk",
            context="Private key file: key.ppk",
            file_type=".ppk",
        )
        result = fix_credential(finding)
        assert result.comment is not None
        assert "remove" in result.comment.lower()


class TestFixCredentialEmail:
    """Email address replacement."""

    def test_email_replaced_with_placeholder(self):
        finding = _make_credential_finding(
            file_path="project-47-django-saas-ecommerce/autoPush.sh",
            matched_text="user@example.com",
            context='git config user.email "user@example.com"',
            file_type=".sh",
        )
        result = fix_credential(finding)
        assert result.action == "replace"
        assert "<EMAIL>" in result.new_text
        assert "user@example.com" not in result.new_text

    def test_email_no_comment_added(self):
        finding = _make_credential_finding(
            file_path="project-47-django-saas-ecommerce/autoPush.sh",
            matched_text="user@example.com",
            context='git config user.email "user@example.com"',
            file_type=".sh",
        )
        result = fix_credential(finding)
        assert result.comment is None

    def test_email_preserves_surrounding_text(self):
        finding = _make_credential_finding(
            file_path="project-47/autoPush.sh",
            matched_text="dev@company.org",
            context='git config user.email "dev@company.org"',
            file_type=".sh",
        )
        result = fix_credential(finding)
        assert 'git config user.email' in result.new_text
        assert "<EMAIL>" in result.new_text


class TestFixCredentialOtherFileTypes:
    """PAT in non-shell, non-YAML files falls back to $GITHUB_TOKEN."""

    def test_pat_in_markdown_uses_github_token(self):
        finding = _make_credential_finding(
            file_path="project-47/README.md",
            context="Use token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij to authenticate",
            file_type=".md",
        )
        result = fix_credential(finding)
        assert "$GITHUB_TOKEN" in result.new_text
        assert "ghp_" not in result.new_text


class TestFixCredentialFallback:
    """Fallback for unrecognised credential types."""

    def test_generic_credential_replaced(self):
        finding = _make_credential_finding(
            matched_text="SOME_SECRET_VALUE",
            context='api_key = "SOME_SECRET_VALUE"',
            file_type=".py",
        )
        result = fix_credential(finding)
        assert result.action == "replace"
        assert "SOME_SECRET_VALUE" not in result.new_text
        assert "<CREDENTIAL>" in result.new_text


# ---------------------------------------------------------------------------
# Account ID fixer tests
# ---------------------------------------------------------------------------


def _make_account_id_finding(
    matched_text: str = "221650130255.dkr.ecr.us-west-2.amazonaws.com",
    context: str = "        image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/devcloudninjas",
    file_path: str = "project-35-devsecops-pipeline-series/step-5-deploy-k8s/deployment.yaml",
    file_type: str = ".yaml",
) -> Finding:
    return Finding(
        file_path=file_path,
        line_number=10,
        matched_text=matched_text,
        issue_type="hardcoded_account_id",
        old_repo_name="",
        context=context,
        file_type=file_type,
    )


class TestFixAccountIdBasic:
    """Basic behaviour of fix_account_id."""

    def test_returns_replacement_with_replace_action(self):
        finding = _make_account_id_finding()
        result = fix_account_id(finding)
        assert result.action == "replace"

    def test_file_path_preserved(self):
        finding = _make_account_id_finding()
        result = fix_account_id(finding)
        assert result.file_path == finding.file_path

    def test_line_number_preserved(self):
        finding = _make_account_id_finding()
        result = fix_account_id(finding)
        assert result.line_number == finding.line_number

    def test_old_text_is_context_line(self):
        finding = _make_account_id_finding()
        result = fix_account_id(finding)
        assert result.old_text == finding.context

    def test_comment_added(self):
        finding = _make_account_id_finding()
        result = fix_account_id(finding)
        assert result.comment == "# Replace <AWS_ACCOUNT_ID> with your AWS account ID"


class TestFixAccountIdReplacement:
    """Verify account ID and image name replacement logic."""

    def test_account_id_replaced_with_placeholder(self):
        finding = _make_account_id_finding(
            context="        image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/devcloudninjas",
        )
        result = fix_account_id(finding)
        assert "221650130255" not in result.new_text
        assert "<AWS_ACCOUNT_ID>" in result.new_text

    def test_image_name_replaced_with_placeholder(self):
        finding = _make_account_id_finding(
            context="        image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/devcloudninjas",
        )
        result = fix_account_id(finding)
        assert "/devcloudninjas" not in result.new_text
        assert "<IMAGE_NAME>" in result.new_text

    def test_ecr_domain_preserved(self):
        finding = _make_account_id_finding(
            context="        image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/devcloudninjas",
        )
        result = fix_account_id(finding)
        assert ".dkr.ecr.us-west-2.amazonaws.com" in result.new_text

    def test_full_replacement_format(self):
        finding = _make_account_id_finding(
            context="        image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/devcloudninjas",
        )
        result = fix_account_id(finding)
        assert "<AWS_ACCOUNT_ID>.dkr.ecr.us-west-2.amazonaws.com/<IMAGE_NAME>" in result.new_text

    def test_ecr_url_without_image_name(self):
        finding = _make_account_id_finding(
            context="  registry: 123456789012.dkr.ecr.eu-west-1.amazonaws.com",
        )
        result = fix_account_id(finding)
        assert "123456789012" not in result.new_text
        assert "<AWS_ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com" in result.new_text

    def test_different_region(self):
        finding = _make_account_id_finding(
            context="  image: 999888777666.dkr.ecr.ap-southeast-1.amazonaws.com/myapp",
        )
        result = fix_account_id(finding)
        assert "<AWS_ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/<IMAGE_NAME>" in result.new_text

    def test_surrounding_text_preserved(self):
        finding = _make_account_id_finding(
            context="        image: 221650130255.dkr.ecr.us-west-2.amazonaws.com/devcloudninjas",
        )
        result = fix_account_id(finding)
        assert result.new_text.startswith("        image: ")


# ---------------------------------------------------------------------------
# Docker image fixer tests
# ---------------------------------------------------------------------------


def _make_docker_image_finding(
    matched_text: str = 'docker.build("devcloudninjas"',
    context: str = '    docker.build("devcloudninjas")',
    file_path: str = "project-35-devsecops-pipeline-series/step-4-docker-ecr/Jenkinsfile",
    file_type: str = "Jenkinsfile",
) -> Finding:
    return Finding(
        file_path=file_path,
        line_number=5,
        matched_text=matched_text,
        issue_type="stale_docker_image",
        old_repo_name="",
        context=context,
        file_type=file_type,
    )


class TestFixDockerImageBasic:
    """Basic behaviour of fix_docker_image."""

    def test_returns_replacement_with_replace_action(self):
        finding = _make_docker_image_finding()
        result = fix_docker_image(finding)
        assert result.action == "replace"

    def test_file_path_preserved(self):
        finding = _make_docker_image_finding()
        result = fix_docker_image(finding)
        assert result.file_path == finding.file_path

    def test_line_number_preserved(self):
        finding = _make_docker_image_finding()
        result = fix_docker_image(finding)
        assert result.line_number == finding.line_number

    def test_old_text_is_context_line(self):
        finding = _make_docker_image_finding()
        result = fix_docker_image(finding)
        assert result.old_text == finding.context

    def test_no_comment_added(self):
        finding = _make_docker_image_finding()
        result = fix_docker_image(finding)
        assert result.comment is None


class TestFixDockerImageBuild:
    """Verify docker.build() call replacement in Jenkinsfiles."""

    def test_docker_build_double_quotes_replaced(self):
        finding = _make_docker_image_finding(
            context='    docker.build("devcloudninjas")',
        )
        result = fix_docker_image(finding)
        assert 'docker.build("<IMAGE_NAME>")' in result.new_text
        assert "devcloudninjas" not in result.new_text

    def test_docker_build_single_quotes_replaced(self):
        finding = _make_docker_image_finding(
            context="    docker.build('devcloudninjas')",
        )
        result = fix_docker_image(finding)
        assert "docker.build('<IMAGE_NAME>')" in result.new_text
        assert "devcloudninjas" not in result.new_text

    def test_docker_build_preserves_surrounding_text(self):
        finding = _make_docker_image_finding(
            context='    def img = docker.build("devcloudninjas")  // build image',
        )
        result = fix_docker_image(finding)
        assert result.new_text.startswith("    def img = ")
        assert result.new_text.endswith("  // build image")

    def test_docker_build_case_insensitive(self):
        finding = _make_docker_image_finding(
            context='    docker.build("DevCloudNinjas")',
        )
        result = fix_docker_image(finding)
        assert "<IMAGE_NAME>" in result.new_text
        assert "DevCloudNinjas" not in result.new_text


class TestFixDockerImageStandalone:
    """Verify standalone image name replacement (YAML, etc.)."""

    def test_yaml_image_field_replaced(self):
        finding = _make_docker_image_finding(
            matched_text="devcloudninjas",
            context="        image: devcloudninjas",
            file_type=".yaml",
        )
        result = fix_docker_image(finding)
        assert result.new_text == "        image: <IMAGE_NAME>"

    def test_standalone_preserves_surrounding_text(self):
        finding = _make_docker_image_finding(
            matched_text="devcloudninjas",
            context="  - name: devcloudninjas  # old image",
            file_type=".yaml",
        )
        result = fix_docker_image(finding)
        assert result.new_text == "  - name: <IMAGE_NAME>  # old image"

    def test_standalone_case_insensitive(self):
        finding = _make_docker_image_finding(
            matched_text="DevCloudNinjas",
            context="        image: DevCloudNinjas",
            file_type=".yaml",
        )
        result = fix_docker_image(finding)
        assert result.new_text == "        image: <IMAGE_NAME>"


# ---------------------------------------------------------------------------
# Go module fixer tests
# ---------------------------------------------------------------------------

from tools.repo_consolidation.fixers import fix_go_module


def _make_gomod_finding(
    file_path: str = "learning/devops-bootcamp/examples/ch7/devops-resources/go.mod",
    line_number: int = 1,
    matched_text: str = "github.com/devcloudninjas/devops-bootcamp",
    context: str = "module github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources",
    old_repo_name: str = "devops-bootcamp",
    file_type: str = ".mod",
) -> Finding:
    return Finding(
        file_path=file_path,
        line_number=line_number,
        matched_text=matched_text,
        issue_type="old_url",
        old_repo_name=old_repo_name,
        context=context,
        file_type=file_type,
    )


class TestFixGoModuleBasic:
    """Basic behaviour of fix_go_module."""

    def test_returns_empty_for_unmapped_repo(self):
        finding = _make_gomod_finding(old_repo_name="nonexistent-repo-xyz")
        result = fix_go_module(finding)
        assert result == []

    def test_returns_empty_for_empty_repo_name(self):
        finding = _make_gomod_finding(old_repo_name="")
        result = fix_go_module(finding)
        assert result == []

    def test_returns_list_of_replacements(self):
        """When go.mod file exists on disk, returns at least one replacement."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create go.mod file
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-resources"
            gomod_dir.mkdir(parents=True)
            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources\n\ngo 1.19\n"
            )

            finding = _make_gomod_finding(
                file_path="learning/devops-bootcamp/examples/ch7/devops-resources/go.mod",
            )
            result = fix_go_module(finding, repo_root=tmpdir)
            assert len(result) >= 1

    def test_replacement_action_is_replace(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-resources"
            gomod_dir.mkdir(parents=True)
            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources\n\ngo 1.19\n"
            )

            finding = _make_gomod_finding()
            result = fix_go_module(finding, repo_root=tmpdir)
            for r in result:
                assert r.action == "replace"


class TestFixGoModuleModulePath:
    """Verify go.mod module path is updated correctly."""

    def test_module_path_updated_to_consolidated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-resources"
            gomod_dir.mkdir(parents=True)
            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources\n\ngo 1.19\n"
            )

            finding = _make_gomod_finding()
            result = fix_go_module(finding, repo_root=tmpdir)
            # The go.mod replacement should update the module path
            gomod_replacements = [r for r in result if r.file_path.endswith("go.mod")]
            assert len(gomod_replacements) >= 1
            assert "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp" in gomod_replacements[0].new_text

    def test_require_directive_also_updated(self):
        """Require directives referencing old repos should also be updated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-api"
            gomod_dir.mkdir(parents=True)
            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module devops-api\n\ngo 1.19\n\nrequire (\n"
                "\tgithub.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources v0.0.0\n)\n"
            )

            finding = _make_gomod_finding(
                file_path="learning/devops-bootcamp/examples/ch7/devops-api/go.mod",
                line_number=6,
                context="\tgithub.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources v0.0.0",
            )
            result = fix_go_module(finding, repo_root=tmpdir)
            gomod_replacements = [r for r in result if r.file_path.endswith("go.mod")]
            assert len(gomod_replacements) >= 1
            updated = gomod_replacements[0].new_text
            assert "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp" in updated


class TestFixGoModuleSourceFiles:
    """Verify sibling .go files are also updated."""

    def test_go_source_import_updated(self):
        """Go source files in the same module should have imports updated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-api"
            gomod_dir.mkdir(parents=True)

            # Create go.mod
            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module devops-api\n\ngo 1.19\n\nrequire (\n"
                "\tgithub.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources v0.0.0\n)\n"
            )

            # Create a .go file with an import referencing the old path
            go_file = gomod_dir / "main.go"
            go_file.write_text(
                'package main\n\nimport (\n'
                '\t"github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources"\n'
                ')\n\nfunc main() {}\n'
            )

            finding = _make_gomod_finding(
                file_path="learning/devops-bootcamp/examples/ch7/devops-api/go.mod",
                line_number=6,
                context="\tgithub.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources v0.0.0",
            )
            result = fix_go_module(finding, repo_root=tmpdir)

            # Should have replacements for both go.mod and main.go
            go_file_replacements = [r for r in result if r.file_path.endswith("main.go")]
            assert len(go_file_replacements) >= 1
            assert "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp" in go_file_replacements[0].new_text

    def test_no_go_source_changes_when_no_old_imports(self):
        """Go files without old import paths should not generate replacements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-resources"
            gomod_dir.mkdir(parents=True)

            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources\n\ngo 1.19\n"
            )

            # Create a .go file with NO old imports
            go_file = gomod_dir / "resource.go"
            go_file.write_text('package resources\n\nimport "fmt"\n\nfunc Hello() { fmt.Println("hi") }\n')

            finding = _make_gomod_finding()
            result = fix_go_module(finding, repo_root=tmpdir)

            go_file_replacements = [r for r in result if r.file_path.endswith("resource.go")]
            assert len(go_file_replacements) == 0


class TestFixGoModuleConsistency:
    """Verify go.mod and Go source files are updated consistently (Property 8)."""

    def test_gomod_and_source_use_same_base_path(self):
        """Both go.mod and .go files should use the same consolidated base path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "ch7" / "devops-api"
            gomod_dir.mkdir(parents=True)

            gomod_file = gomod_dir / "go.mod"
            gomod_file.write_text(
                "module devops-api\n\ngo 1.19\n\nrequire (\n"
                "\tgithub.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources v0.0.0\n)\n"
            )

            go_file = gomod_dir / "main.go"
            go_file.write_text(
                'package main\n\nimport (\n'
                '\t"github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources"\n'
                ')\n\nfunc main() {}\n'
            )

            finding = _make_gomod_finding(
                file_path="learning/devops-bootcamp/examples/ch7/devops-api/go.mod",
                line_number=6,
                context="\tgithub.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources v0.0.0",
            )
            result = fix_go_module(finding, repo_root=tmpdir)

            gomod_replacements = [r for r in result if r.file_path.endswith("go.mod")]
            go_replacements = [r for r in result if r.file_path.endswith("main.go")]

            assert len(gomod_replacements) >= 1
            assert len(go_replacements) >= 1

            # Both should reference the same consolidated base
            consolidated_base = "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp"
            assert consolidated_base in gomod_replacements[0].new_text
            assert consolidated_base in go_replacements[0].new_text

    def test_fallback_when_gomod_unreadable(self):
        """When go.mod can't be read from disk, falls back to fixing the finding line."""
        finding = _make_gomod_finding()
        # Use a repo_root that doesn't contain the file
        with tempfile.TemporaryDirectory() as tmpdir:
            result = fix_go_module(finding, repo_root=tmpdir)
            assert len(result) == 1
            assert "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp" in result[0].new_text


class TestFixGoModuleExampleTestGo:
    """Verify handling of the specific example_test.go file from requirements."""

    def test_example_test_go_urls_updated(self):
        """The example_test.go file has URLs in test data that should be updated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create the go.mod and example_test.go structure
            gomod_dir = Path(tmpdir) / "learning" / "devops-bootcamp" / "examples" / "codeQuality" / "goExamples"
            gomod_dir.mkdir(parents=True)

            # Create a minimal go.mod in a parent directory
            parent_mod_dir = Path(tmpdir) / "learning" / "devops-bootcamp"
            (parent_mod_dir / "go.mod").write_text(
                "module github.com/devcloudninjas/devops-bootcamp\n\ngo 1.19\n"
            )

            # Create example_test.go with old URLs
            test_file = gomod_dir / "example_test.go"
            test_file.write_text(
                'package go_unit_test_bootcamp\n\n'
                'import "testing"\n\n'
                'func TestBasic(t *testing.T) {\n'
                '\turl := "https://github.com/devcloudninjas/devops-bootcamp"\n'
                '}\n'
            )

            finding = _make_gomod_finding(
                file_path="learning/devops-bootcamp/go.mod",
                context="module github.com/devcloudninjas/devops-bootcamp",
            )
            result = fix_go_module(finding, repo_root=tmpdir)

            # Should have a replacement for go.mod
            gomod_replacements = [r for r in result if r.file_path.endswith("go.mod")]
            assert len(gomod_replacements) >= 1
            assert "DevOps-Projects/learning/devops-bootcamp" in gomod_replacements[0].new_text
