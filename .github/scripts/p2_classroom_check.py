#!/usr/bin/env python3
"""Validate the minimum classroom evidence contract for all active projects."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "config" / "active-integrity-manifest.json"
REQUIRED = ("P2_CLASSROOM.md", "P2_EVIDENCE.md", "P2_LOCAL_PILOT.md", "START_HERE.md")


def main() -> int:
    projects = json.loads(MANIFEST.read_text(encoding="utf-8"))["projects"]
    failures: list[str] = []
    for entry in projects:
        root = ROOT / entry["project"]
        for name in REQUIRED:
            if not (root / name).is_file():
                failures.append(f"{entry['project']}/{name}")
        classroom = root / "P2_CLASSROOM.md"
        if (
            classroom.is_file()
            and "## Learning and assessment"
            not in classroom.read_text(encoding="utf-8")
        ):
            failures.append(
                f"{entry['project']}/P2_CLASSROOM.md missing Learning and assessment"
            )
    if failures:
        print(
            "ERROR: classroom contract failures: " + ", ".join(failures),
            file=sys.stderr,
        )
        return 1
    print(f"P2 classroom contract: PASS ({len(projects)} projects)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
