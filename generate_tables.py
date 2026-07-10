import csv, json
from pathlib import Path
from nlca.security_analysis import sbox_metrics
from nlca.baselines import baseline_manifest

out=Path("results"); out.mkdir(exist_ok=True)
with (out/"table_sbox_metrics.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["metric","value"])
    for k,v in sbox_metrics().items(): w.writerow([k,json.dumps(v)])
with (out/"table_baseline_provenance.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["algorithm","category","provenance"])
    for k,v in baseline_manifest().items(): w.writerow([k,v["category"],v["provenance"]])
print("Tables generated in results/")
