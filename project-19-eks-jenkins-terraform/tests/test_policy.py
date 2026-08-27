from pathlib import Path


def test_local_classroom_prerequisites() -> None:
    root = next(
        path
        for path in Path(__file__).resolve().parents
        if path.name == "project-19-eks-jenkins-terraform"
    )
    assert (root / "README.md").is_file()
    assert (root / "START_HERE.md").is_file()
