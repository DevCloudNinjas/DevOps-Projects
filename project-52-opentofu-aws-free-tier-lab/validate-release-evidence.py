#!/usr/bin/env python3
"""Deterministic local-only helper for project-52-opentofu-aws-free-tier-lab."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
if ROOT.name != "project-52-opentofu-aws-free-tier-lab":
    raise SystemExit("ERROR: project root mismatch")
for name in (
    "README.md",
    "START_HERE.md",
    "P2_CLASSROOM.md",
    "P2_EVIDENCE.md",
    "P2_LOCAL_PILOT.md",
):
    if not (ROOT / name).is_file():
        raise SystemExit(f"ERROR: missing {name}")
print(
    "project-52-opentofu-aws-free-tier-lab local-only control: PASS (validate-release-evidence.py)"
)
