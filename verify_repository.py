import subprocess, sys
from nlca.verification import verify_core

checks=[]
try:
    verify_core(); checks.append("[PASS] core cryptographic verification")
except Exception as e:
    checks.append(f"[FAIL] core cryptographic verification: {e}")
result=subprocess.run([sys.executable,"-m","pytest","-q"],capture_output=True,text=True)
checks.append("[PASS] pytest suite" if result.returncode==0 else "[FAIL] pytest suite")
print("\n".join(checks))
if result.returncode:
    print(result.stdout); print(result.stderr); raise SystemExit(1)
