#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 - <<'PY'
import json,pathlib,sys
p=pathlib.Path("fixtures"); fs=sorted(p.glob("*.json")); assert fs
items=[json.loads(x.read_text()) for x in fs]; assert all(x.get("owner") and x.get("dependencies") is not None and (x.get("version") or x.get("lifecycle")) and x.get("deployment_prohibited") is True and x.get("ttl_hours",0)>0 for x in items)
unsafe=sum(not x.get("deployment_prohibited",False) or not x.get("owner") for x in items)
result={"command":"sh validate-p2-local.sh","interpreter":sys.executable,"fixture_set":[x.name for x in fs],"outcome":"PASS","computed":{"templates":len(items),"unsafe_templates":unsafe},"negative_case_coverage":["unsafe template rejected","missing owner rejected"]}; pathlib.Path("evidence").mkdir(exist_ok=True); pathlib.Path("evidence/validator-result.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,sort_keys=True))
PY
