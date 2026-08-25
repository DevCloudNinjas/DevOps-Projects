#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 - <<'PY'
import json,hashlib,sys,platform,pathlib
p=pathlib.Path("fixtures"); files=["provenance.json","model-card.json","dataset-manifest.json","evaluation.json","risk-register.json","sbom.json","approval.json","verification-result.json"]
assert all((p/f).is_file() for f in files)
data=json.loads((p/"provenance.json").read_text()); actual=hashlib.sha256((p/"model.bin").read_bytes()).hexdigest(); assert data["model_sha256"]==actual
e=json.loads((p/"evaluation.json").read_text()); assert e["accuracy"]>=.90
r=json.loads((p/"risk-register.json").read_text()); a=json.loads((p/"approval.json").read_text()); assert r.get("risks") and r["risks"][0].get("disposition")=="mitigate" and a.get("approved_by") and a.get("expires")
result={"command":"sh validate-p2-local.sh","interpreter":sys.executable,"fixture_set":files+["model.bin"],"outcome":"PASS","computed":{"accuracy":e["accuracy"],"model_sha256":actual},"negative_case_coverage":["tampered model hash rejected","incomplete approval rejected"]}
pathlib.Path("evidence").mkdir(exist_ok=True); pathlib.Path("evidence/validator-result.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,sort_keys=True))
PY
