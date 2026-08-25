#!/usr/bin/env python3
"""Validate the checked-in L2 Live Pilot Execution Pack without external access."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs" / "live-pilot-execution-pack"
REQUIRED = {
    "README.md": (
        "project-53-supply-chain-security-lab",
        "source-only",
        "not authorization",
    ),
    "AUTHORIZATION_RECORD.md": ("approval", "budget", "window"),
    "PILOT_RUNBOOK.md": ("stop condition", "evidence", "teardown"),
    "PREFLIGHT_CHECKLIST.md": ("fail-closed", "external", "identity"),
    "EVIDENCE_INDEX.md": ("authorization", "teardown", "residual"),
    "EVIDENCE_RECORD_TEMPLATE.md": ("provenance", "reviewer", "redaction"),
    "TEARDOWN_AND_RESIDUAL_COST_CHECKLIST.md": ("inventory", "residual", "cost"),
    "RACI.md": ("accountable", "operator", "reviewer"),
    "RISK_ROLLBACK_GUIDANCE.md": ("rollback", "stop", "escalation"),
    "EXTERNAL_PREREQUISITES.md": ("github", "cloud", "external"),
    "ACCEPTANCE_CRITERIA.md": ("ready", "source-only", "project 53"),
    "CLOSURE_RECORD.md": ("not authorization", "residual", "reviewer"),
}
LOCAL_LINK = re.compile(r"\[[^]]*\]\(([^)#]+)(?:#[^)]+)?\)")
FORBIDDEN_CLAIMS = re.compile(
    r"(?im)^\s*(?:status|approval state)\s*:\s*(?:approved|authorized|executed|complete)\s*$|"
    r"\b(?:live pilot|deployment|teardown)\s+(?:completed|succeeded)\b"
)


def fail(message: str) -> None:
    print(f"L2 execution pack blocked: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not PACK.is_dir():
        fail("execution-pack directory is missing")
    all_text: list[str] = []
    for name, markers in REQUIRED.items():
        path = PACK / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            fail(f"required document missing or empty: {name}")
        text = path.read_text(encoding="utf-8")
        normalized = text.lower()
        missing = [marker for marker in markers if marker not in normalized]
        if missing:
            fail(f"{name} lacks required markers: {', '.join(missing)}")
        for target in LOCAL_LINK.findall(text):
            if "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / target).resolve().is_file():
                fail(f"broken internal link: {name} -> {target}")
        all_text.append(text)
    joined = "\n".join(all_text)
    if (
        "project-52-opentofu-aws-free-tier-lab" not in joined.lower()
        or "reusable source-only" not in joined.lower()
    ):
        fail("Project 52 reusable-pattern boundary is missing")
    if FORBIDDEN_CLAIMS.search(joined):
        fail("pack contains an unsupported live authorization or completion claim")
    print("L2 Live Pilot Execution Pack validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
