#!/usr/bin/env python3
"""Validate the two checked-in L2 pilot patterns without cloud access."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOTS = {
    "project-52-opentofu-aws-free-tier-lab": "reusable",
    "project-53-supply-chain-security-lab": "sole selected pilot",
}
FORBIDDEN = re.compile(
    r"id-token\s*:\s*write|aws-actions|azure/login|"
    r"google-github-actions|\b(?:terraform|tofu)\s+(?:apply|destroy)|"
    r"\bkubectl\s+(?:apply|delete)|\bdocker\s+push|"
    r"\b(?:provider|cloud)\s+login\b|\bsecrets\.",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    print(f"L2 pilot validation blocked: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    for project, boundary in PILOTS.items():
        root = ROOT / project
        readme = root / "pilot" / "README.md"
        workflow = root / ".github" / "workflows" / "l2-cloud-pilot.yml"
        source_gates = root / ".github" / "workflows" / "l2-source-gates.yml"
        if not readme.is_file() or not workflow.is_file() or not source_gates.is_file():
            fail(f"{project}: required pilot files are missing")
        if boundary not in readme.read_text(encoding="utf-8").lower():
            fail(f"{project}: pilot boundary is not explicit")
        for path in (workflow, source_gates):
            text = path.read_text(encoding="utf-8")
            if FORBIDDEN.search(text):
                fail(f"{project}: forbidden cloud execution surface in {path.name}")
    print("L2 pilot validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
