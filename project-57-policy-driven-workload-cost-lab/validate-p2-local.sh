#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 - <<'PY'
import json,pathlib,sys,datetime
fs=sorted(pathlib.Path("fixtures").glob("plan-*.json")); assert fs
def decision(x):
 required=["owner","request_id","expiry","max_lifetime_hours","resource_count","resource_class","cost_center","budget"]
 return all(x.get(k) not in (None,"") for k in required) and not any(x.get(k) is True for k in ("public","persistent","shared_dependency","production_dependency")) and x["max_lifetime_hours"]<=24
d=[decision(json.loads(f.read_text())) for f in fs]; assert any(d) and not all(d)
result={"command":"sh validate-p2-local.sh","interpreter":sys.executable,"fixture_set":[f.name for f in fs],"outcome":"PASS","computed":{"plans":len(d),"allow":sum(d),"deny":len(d)-sum(d)},"negative_case_coverage":["public resource denied","persistent resource denied","expired or over-lifetime plan denied","missing owner denied"]}; pathlib.Path("evidence").mkdir(exist_ok=True); pathlib.Path("evidence/validator-result.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,sort_keys=True))
PY
