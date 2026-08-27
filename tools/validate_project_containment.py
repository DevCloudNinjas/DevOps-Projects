#!/usr/bin/env python3
"""Fail closed when active project content escapes its root or links to quarantine."""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_project_containment.py PROJECT_ROOT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.name.startswith("project-") or not root.is_dir():
        print("ERROR: expected a project root", file=sys.stderr)
        return 1
    for path in root.rglob("*"):
        if path.is_symlink():
            try:
                path.resolve().relative_to(root)
            except ValueError:
                print(f"ERROR: path escapes project root: {path}", file=sys.stderr)
                return 1
        if path.suffix.lower() == ".md" and "quarantine/" in path.read_text(encoding="utf-8", errors="ignore"):
            print(f"ERROR: active Markdown references quarantine: {path}", file=sys.stderr)
            return 1
    print(f"Project containment: PASS ({root.name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
