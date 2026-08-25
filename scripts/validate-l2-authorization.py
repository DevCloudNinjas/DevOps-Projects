#!/usr/bin/env python3
"""Validate a synthetic L2 authorization fixture without external access."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {"project", "state", "reviewer", "window"}


def fail(message: str) -> None:
    print(f"L2 authorization fixture blocked: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if len(sys.argv) != 2:
        fail("expected one fixture path")
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"invalid JSON fixture: {error}")
    if not REQUIRED.issubset(data):
        fail("missing required synthetic authorization fields")
    if data["state"] != "synthetic-source-validation-only":
        fail("fixture must not represent a live approval")
    if not isinstance(data["project"], str) or not data["project"].startswith(
        "project-"
    ):
        fail("fixture project identifier is invalid")
    print("L2 authorization fixture validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
