#!/usr/bin/env python3
"""Validate a synthetic L2 evidence fixture without external access."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {"project", "outcome", "teardown_state", "residual_state"}


def fail(message: str) -> None:
    print(f"L2 evidence fixture blocked: {message}", file=sys.stderr)
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
        fail("missing required synthetic evidence fields")
    if data["outcome"] != "synthetic-source-validation-only":
        fail("fixture must not represent live evidence")
    if data["teardown_state"] != "not-executed":
        fail("fixture must not claim teardown execution")
    if data["residual_state"] != "not-executed":
        fail("fixture must not claim residual verification")
    print("L2 evidence fixture validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
