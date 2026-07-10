import json
from pathlib import Path
from nlca.security_analysis import reduced_round_report

key=bytes.fromhex("000102030405060708090a0b0c0d0e0f")
pt=bytes.fromhex("00112233445566778899aabbccddeeff")
rows=reduced_round_report(key,pt,12)
Path("results").mkdir(exist_ok=True)
Path("results/round_analysis.json").write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
