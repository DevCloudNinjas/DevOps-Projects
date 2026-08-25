#!/usr/bin/env python3
"""Validate the source-only L2 pilot contract without cloud access or execution."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOTS = (
    ("project-52-opentofu-aws-free-tier-lab", False),
    ("project-53-supply-chain-security-lab", True),
)
FORBIDDEN_WORKFLOW = re.compile(
    r"id-token\s*:\s*write|aws-actions|azure/login|google-github-actions|"
    r"\b(?:terraform|tofu)\s+(?:apply|destroy)|"
    r"\bkubectl\s+(?:apply|delete)|\bdocker\s+push|"
    r"\b(?:teardown|provider\s+login|cloud\s+login)\b|"
    r"\bsecrets\.|AKIA[0-9A-Z]{16}|\b[0-9]{12}\b|https?://",
    re.IGNORECASE,
)
REQUIRED_POLICY_TERMS = (
    "allow",
    "region",
    "ttl",
    "public",
    "persistent",
    "tag",
    "wildcard",
    "shared",
    "production",
    "owner",
    "expiry",
)


def fail(message: str) -> None:
    print(f"L2 source contract blocked: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_validator(script: str, fixture: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), str(fixture)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        fail(f"{script} rejected {fixture.relative_to(ROOT)}: {result.stderr.strip() or result.stdout.strip()}")


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate-l2-cloud-pilots.py")], cwd=ROOT, check=True)
    for project, selected in PILOTS:
        root = ROOT / project
        workflow = root / ".github" / "workflows" / "l2-cloud-pilot-source-contract.yml"
        text = workflow.read_text(encoding="utf-8")
        if "source contract" not in text.lower() or FORBIDDEN_WORKFLOW.search(text):
            fail(f"{project}: optional workflow is not a local source-only contract")
        if selected and "sole selected pilot" not in (root / "pilot" / "README.md").read_text(encoding="utf-8").lower():
            fail(f"{project}: selected-pilot boundary is not explicit")
        if not selected and "reusable" not in (root / "pilot" / "README.md").read_text(encoding="utf-8").lower():
            fail(f"{project}: reusable-pattern boundary is not explicit")
        policy = (root / "pilot" / "policy.rego").read_text(encoding="utf-8").lower()
        missing = [term for term in REQUIRED_POLICY_TERMS if term not in policy]
        if missing:
            fail(f"{project}: policy lacks required deny/control terms: {', '.join(missing)}")
        fixture_dir = root / "fixtures" / "l2-source-contract"
        run_validator("validate-l2-authorization.py", fixture_dir / "authorization-valid.json")
        run_validator("validate-l2-evidence.py", fixture_dir / "evidence-valid.json")
        schema = json.loads((root / "pilot" / "authorization-schema.json").read_text(encoding="utf-8"))
        if not schema.get("required"):
            fail(f"{project}: authorization schema has no required fields")
    print("L2 source contract validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
