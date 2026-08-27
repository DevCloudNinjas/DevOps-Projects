#!/usr/bin/env python3
"""Fail-closed validation of the manifest-declared active classroom surface."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "active-integrity-manifest.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not MANIFEST.is_file():
        fail("missing active-integrity manifest")
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    projects = payload.get("projects")
    if not isinstance(projects, list) or not projects:
        fail("manifest projects list is missing or empty")
    declared: set[str] = set()
    for entry in projects:
        if not isinstance(entry, dict):
            fail("manifest project entry is not an object")
        project = entry.get("project")
        active_files = entry.get("active_files")
        quarantine = entry.get("quarantine_root", "quarantine")
        if not isinstance(project, str) or not project.startswith("project-"):
            fail("invalid project name in manifest")
        if project in declared:
            fail(f"duplicate manifest project: {project}")
        declared.add(project)
        root = ROOT / project
        if not root.is_dir():
            fail(f"missing declared project root: {project}")
        if not isinstance(active_files, list) or not active_files:
            fail(f"missing active file list for {project}")
        for rel in active_files:
            if not isinstance(rel, str) or not rel or rel.startswith("/") or ".." in Path(rel).parts:
                fail(f"unsafe declared active path for {project}: {rel!r}")
            target = root / rel
            if not target.exists() or not target.is_file():
                fail(f"missing declared active file: {project}/{rel}")
            if target.is_symlink():
                resolved = target.resolve()
                try:
                    resolved.relative_to(root.resolve())
                except ValueError:
                    fail(f"active file escapes project root: {project}/{rel}")
            if quarantine and (root / quarantine) in target.parents:
                fail(f"manifest declares quarantined file as active: {project}/{rel}")
        for markdown in root.rglob("*.md"):
            if quarantine and quarantine + "/" in markdown.read_text(encoding="utf-8", errors="ignore"):
                fail(f"active Markdown references quarantine: {markdown.relative_to(ROOT)}")
    actual = {path.name for path in ROOT.glob("project-*") if path.is_dir()}
    if actual != declared:
        missing = sorted(declared - actual)
        extra = sorted(actual - declared)
        fail(f"manifest/project inventory mismatch; missing={missing}, extra={extra}")
    print(f"Active integrity validation: PASS ({len(declared)} projects)")


if __name__ == "__main__":
    main()
