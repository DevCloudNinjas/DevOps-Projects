"""Tests for the URL mapping registry."""

from tools.repo_consolidation.url_map import (
    CONSOLIDATED_CLONE_URL,
    CONSOLIDATED_TREE_URL,
    URL_MAP,
    compute_relative_path,
    is_mapped,
    lookup,
    resolve_new_path,
)


class TestURLMap:
    """Basic correctness tests for the static URL_MAP and lookup helpers."""

    def test_map_has_minimum_entries(self) -> None:
        """URL_MAP should contain at least 58 entries (all consolidated repos)."""
        assert len(URL_MAP) >= 58

    # -- Known mappings from requirements ----------------------------------

    def test_zomato_clone(self) -> None:
        assert URL_MAP["Zomato-Clone"] == "project-13-zomato-clone-devsecops"

    def test_tetris_project(self) -> None:
        assert URL_MAP["Complete-Kubernetes-DevSecOps-Tetris-Project"] == "project-32-tetris-devsecops-k8s"

    def test_blog_app(self) -> None:
        assert URL_MAP["full-stack-blogging-app"] == "project-30-blog-app-eks"

    def test_super_mario(self) -> None:
        assert URL_MAP["Deployment-of-super-Mario-on-Kubernetes-using-terraform"] == "project-12-super-mario-k8s"

    def test_devops_bootcamp(self) -> None:
        assert URL_MAP["devops-bootcamp"] == "learning/devops-bootcamp"

    def test_cka_prep(self) -> None:
        assert URL_MAP["Certified_Kubernetes_Administrator"] == "learning/kubernetes-cka-prep"

    def test_devops_tools(self) -> None:
        assert URL_MAP["devops-tools"] == "resources/devops-tools-list"

    def test_github_examples(self) -> None:
        assert URL_MAP["Github-Examples"] == "resources/github-actions-examples"

    # -- Case-insensitive lookup -------------------------------------------

    def test_lookup_exact_case(self) -> None:
        assert lookup("Zomato-Clone") == "project-13-zomato-clone-devsecops"

    def test_lookup_lower_case(self) -> None:
        assert lookup("zomato-clone") == "project-13-zomato-clone-devsecops"

    def test_lookup_upper_case(self) -> None:
        assert lookup("ZOMATO-CLONE") == "project-13-zomato-clone-devsecops"

    def test_lookup_mixed_case(self) -> None:
        assert lookup("devops-bootcamp") == "learning/devops-bootcamp"
        assert lookup("DEVOPS-BOOTCAMP") == "learning/devops-bootcamp"

    def test_lookup_unmapped_returns_none(self) -> None:
        assert lookup("nonexistent-repo") is None

    def test_lookup_devops_projects_not_in_map(self) -> None:
        """The consolidated repo itself should NOT be in the map."""
        assert lookup("DevOps-Projects") is None

    # -- is_mapped ---------------------------------------------------------

    def test_is_mapped_true(self) -> None:
        assert is_mapped("Zomato-Clone") is True
        assert is_mapped("zomato-clone") is True

    def test_is_mapped_false(self) -> None:
        assert is_mapped("nonexistent-repo") is False

    # -- Category coverage -------------------------------------------------

    def test_all_project_folders_01_to_30_mapped(self) -> None:
        for i in range(1, 31):
            key = f"DevOps-Project-{i:02d}"
            assert key in URL_MAP, f"Missing mapping for {key}"

    def test_learning_repos_mapped(self) -> None:
        learning_repos = [
            "devops-bootcamp",
            "Certified_Kubernetes_Administrator",
            "kubernetes-learning-path",
            "Kubernetes-101",
            "Containers_Fundamental_HandsOn",
            "Docker_HandsOn_Training",
            "DevOps_101_Projects",
            "DevOps_201_Projects",
            "DevOps_Random_Projects",
            "Learning-Prometheus",
            "Linux-Hands-On",
            "into-the-devops",
            "sre-interview-prep-guide",
            "DevOps_Setup-Installations",
        ]
        for repo in learning_repos:
            assert repo in URL_MAP, f"Missing learning repo mapping: {repo}"
            assert URL_MAP[repo].startswith("learning/"), f"{repo} should map to learning/"

    def test_resource_repos_mapped(self) -> None:
        resource_repos = ["devops-tools", "Github-Examples", "coding-interview-university"]
        for repo in resource_repos:
            assert repo in URL_MAP, f"Missing resource repo mapping: {repo}"
            assert URL_MAP[repo].startswith("resources/"), f"{repo} should map to resources/"

    def test_asecguru_series_mapped(self) -> None:
        for i in range(1, 7):
            found = any(
                v.startswith(f"project-35-devsecops-pipeline-series/step-{i}")
                for v in URL_MAP.values()
            )
            assert found, f"Missing asecguru step {i} mapping"


class TestComputeRelativePath:
    """Tests for compute_relative_path — POSIX relative path computation."""

    def test_sibling_directories(self) -> None:
        result = compute_relative_path("project-13/README.md", "project-30/README.md")
        assert result == "../project-30/README.md"

    def test_same_directory(self) -> None:
        result = compute_relative_path("learning/k8s/README.md", "learning/k8s/docs/setup.md")
        assert result == "docs/setup.md"

    def test_root_to_nested(self) -> None:
        result = compute_relative_path("README.md", "project-13/README.md")
        assert result == "project-13/README.md"

    def test_nested_to_root(self) -> None:
        result = compute_relative_path("project-13/docs/guide.md", "README.md")
        assert result == "../../README.md"

    def test_deep_traversal(self) -> None:
        result = compute_relative_path(
            "project-35/step-1/infra/main.tf",
            "learning/devops-bootcamp/README.md",
        )
        assert result == "../../../learning/devops-bootcamp/README.md"

    def test_same_file_directory(self) -> None:
        """Target in the same directory as source file."""
        result = compute_relative_path("docs/a.md", "docs/b.md")
        assert result == "b.md"

    def test_uses_forward_slashes(self) -> None:
        result = compute_relative_path("a/b/c.md", "x/y/z.md")
        assert "\\" not in result
        assert result == "../../x/y/z.md"

    def test_target_is_directory(self) -> None:
        """to_path can be a directory (no extension)."""
        result = compute_relative_path(
            "project-13/README.md",
            "project-13-zomato-clone-devsecops",
        )
        assert result == "../project-13-zomato-clone-devsecops"


class TestResolveNewPath:
    """Tests for resolve_new_path — context-aware replacement logic."""

    # -- Unmapped repo returns None ----------------------------------------

    def test_unmapped_repo_returns_none(self) -> None:
        result = resolve_new_path(
            "nonexistent-repo",
            "https://github.com/DevCloudNinjas/nonexistent-repo",
            "README.md",
        )
        assert result is None

    # -- Clone URL context -------------------------------------------------

    def test_git_clone_url(self) -> None:
        result = resolve_new_path(
            "Zomato-Clone",
            "git clone https://github.com/DevCloudNinjas/Zomato-Clone.git",
            "project-13/README.md",
        )
        assert result == CONSOLIDATED_CLONE_URL

    def test_dot_git_suffix(self) -> None:
        result = resolve_new_path(
            "full-stack-blogging-app",
            "https://github.com/DevCloudNinjas/full-stack-blogging-app.git",
            "project-30/README.md",
        )
        assert result == CONSOLIDATED_CLONE_URL

    # -- Config metadata context -------------------------------------------

    def test_package_json_returns_tree_url(self) -> None:
        result = resolve_new_path(
            "devops-bootcamp",
            "https://github.com/devcloudninjas/devops-bootcamp",
            "learning/devops-bootcamp/package.json",
        )
        assert result == f"{CONSOLIDATED_TREE_URL}/learning/devops-bootcamp"

    def test_package_json_case_insensitive_filename(self) -> None:
        """Source file matching should work regardless of path casing."""
        result = resolve_new_path(
            "devops-bootcamp",
            "https://github.com/devcloudninjas/devops-bootcamp",
            "learning/devops-bootcamp/Package.json",
        )
        assert result == f"{CONSOLIDATED_TREE_URL}/learning/devops-bootcamp"

    # -- In-repo relative path context (default) ---------------------------

    def test_readme_relative_path(self) -> None:
        result = resolve_new_path(
            "Zomato-Clone",
            "https://github.com/DevCloudNinjas/Zomato-Clone",
            "project-13/README.md",
        )
        # project-13/README.md → project-13-zomato-clone-devsecops
        assert result == "../project-13-zomato-clone-devsecops"

    def test_learning_doc_relative_path(self) -> None:
        result = resolve_new_path(
            "Certified_Kubernetes_Administrator",
            "https://github.com/DevCloudNinjas/Certified_Kubernetes_Administrator",
            "learning/kubernetes-cka-prep/README.md",
        )
        # Same directory — target is "learning/kubernetes-cka-prep"
        assert result == "."

    def test_cross_section_relative_path(self) -> None:
        result = resolve_new_path(
            "devops-tools",
            "https://github.com/DevCloudNinjas/devops-tools",
            "project-13/README.md",
        )
        assert result == "../resources/devops-tools-list"
