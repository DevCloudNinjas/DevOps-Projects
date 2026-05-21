import json
import subprocess
from pathlib import Path

from tools.project_inventory import (
    LEARNER_BADGES,
    LEARNING_PATHS,
    Project,
    discover_projects,
    list_main,
    projects_for_changed_files,
    validate_metadata,
    validate_project,
)


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _write_metadata(repo: Path) -> None:
    metadata = {
        "project_roots": [
            {
                "name": "test-projects",
                "glob": "project-*",
            },
        ],
        "validation": {
            "quality_gate": "python -m tools.quality_gate --project {project} .",
        },
    }
    tools_dir = repo / "tools"
    tools_dir.mkdir(exist_ok=True)
    tools_dir.joinpath("project_metadata.json").write_text(
        json.dumps(metadata), encoding="utf-8"
    )


def test_discover_projects_from_metadata(tmp_path: Path) -> None:
    (tmp_path / "project-02-beta").mkdir()
    (tmp_path / "project-01-alpha").mkdir()
    (tmp_path / "learning").mkdir()
    _write_metadata(tmp_path)

    projects = discover_projects(tmp_path)

    assert [project.path for project in projects] == [
        "project-01-alpha",
        "project-02-beta",
    ]
    assert projects[0].id == "project-01-alpha"


def test_validate_metadata_rejects_parent_glob(tmp_path: Path) -> None:
    metadata = {"project_roots": [{"glob": "../*"}]}

    errors = validate_metadata(tmp_path, metadata)

    assert any("inside the repository" in error for error in errors)


def test_validate_metadata_accepts_learner_conventions(tmp_path: Path) -> None:
    (tmp_path / "project-01-alpha").mkdir()
    metadata = {
        "project_roots": [{"glob": "project-*"}],
        "learner_metadata": {
            "learning_paths": list(LEARNING_PATHS),
            "badges": list(LEARNER_BADGES),
        },
    }

    errors = validate_metadata(tmp_path, metadata)

    assert errors == []


def test_validate_metadata_rejects_unknown_learner_badges(tmp_path: Path) -> None:
    (tmp_path / "project-01-alpha").mkdir()
    metadata = {
        "project_roots": [{"glob": "project-*"}],
        "learner_metadata": {
            "learning_paths": ["kubernetes"],
            "badges": ["mystery-badge"],
        },
    }

    errors = validate_metadata(tmp_path, metadata)

    assert any("learner_metadata.badges" in error for error in errors)


def test_projects_for_changed_files_maps_nested_paths() -> None:
    projects = [
        Project(
            id="one",
            path="project-01-alpha",
            name="project-01-alpha",
            source="test",
        ),
        Project(
            id="two",
            path="project-02-beta",
            name="project-02-beta",
            source="test",
        ),
    ]

    changed = projects_for_changed_files(
        projects,
        ["README.md", "project-02-beta/app/main.py", "project-02-beta/README.md"],
    )

    assert [project.path for project in changed] == ["project-02-beta"]


def test_list_main_outputs_github_matrix_for_changed_projects(
    tmp_path: Path, capsys
) -> None:
    _run(["git", "init"], tmp_path)
    _run(["git", "config", "user.email", "test@example.com"], tmp_path)
    _run(["git", "config", "user.name", "Test User"], tmp_path)
    _write_metadata(tmp_path)
    project = tmp_path / "project-01-alpha"
    project.mkdir()
    project.joinpath("README.md").write_text("hello\n", encoding="utf-8")
    _run(["git", "add", "-A"], tmp_path)
    _run(["git", "commit", "-m", "initial"], tmp_path)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    project.joinpath("README.md").write_text("hello again\n", encoding="utf-8")
    _run(["git", "add", "-A"], tmp_path)
    _run(["git", "commit", "-m", "change project"], tmp_path)

    result = list_main(
        [
            "--repo-root",
            str(tmp_path),
            "--changed-from",
            base,
            "--format",
            "github-matrix",
        ],
    )

    assert result == 0
    matrix = json.loads(capsys.readouterr().out)
    assert matrix["include"][0]["path"] == "project-01-alpha"


def test_validate_project_rejects_unknown_project(tmp_path: Path, capsys) -> None:
    _write_metadata(tmp_path)
    (tmp_path / "project-01-alpha").mkdir()

    result = validate_project(tmp_path, "project-99-missing")

    assert result == 2
    assert "Unknown project" in capsys.readouterr().out
