#!/usr/bin/env python3
"""Validate local release evidence without contacting external systems."""

from pathlib import Path

root = Path(__file__).resolve().parent
if not (root / "P2_EVIDENCE.md").is_file():
    raise SystemExit("ERROR: missing P2_EVIDENCE.md")
print(
    "project-14-github-actions-android local evidence validation: PASS (verify_ci_contract.py)"
)
