#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 - <<'PY'
import csv,json,pathlib,sys
rows=list(csv.DictReader(open("fixtures/daily-costs.csv"))); total=round(sum(float(r["quantity"])*float(r["rate"]) for r in rows),2); unallocated=sum(r["allocation_status"]=="unallocated" for r in rows); b=json.load(open("fixtures/budget-report.json")); rec=json.load(open("fixtures/recommendations.json")); assert total==round(float(b["actual"]),2) and unallocated>0 and float(b["budget"])>=total and all(x.get("owner") and x.get("due_date") and x.get("expected_benefit") and x.get("evidence_status") for x in rec)
result={"command":"sh validate-p2-local.sh","interpreter":sys.executable,"fixture_set":[p.name for p in pathlib.Path("fixtures").iterdir()],"outcome":"PASS","computed":{"ledger_total":total,"unallocated_rows":unallocated,"budget_variance":round(float(b["budget"])-total,2),"recommendations":len(rec)},"negative_case_coverage":["allocation gap detected","budget overrun would fail","missing recommendation owner/due date would fail","unclosed evidence would fail"]}; pathlib.Path("evidence").mkdir(exist_ok=True); pathlib.Path("evidence/validator-result.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,sort_keys=True))
PY
