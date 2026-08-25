#!/usr/bin/env python3
import json
import re
from pathlib import Path

r = Path(__file__).resolve().parents[1]
m = json.loads((r / "config/active-integrity-manifest.json").read_text())
entries = m["projects"]
names = {x["project"] for x in entries}
assert {
    "project-52-opentofu-aws-free-tier-lab",
    "project-53-supply-chain-security-lab",
}.issubset(names)
assert (
    "sole selected pilot"
    in (r / "project-53-supply-chain-security-lab/pilot/README.md").read_text().lower()
)
assert "project-52-opentofu-aws-free-tier-lab" in json.dumps(m).lower()
text = "\n".join(
    p.read_text(errors="ignore") for p in r.glob("project-5[5-8]-*/**/*.md")
)
assert not re.search(
    r"project[- ]52.{0,80}\b(selected|live|repurposed)\b", text, re.I | re.S
)
print("PASS emerging packet: manifest roots and L2/source-only boundaries verified")
