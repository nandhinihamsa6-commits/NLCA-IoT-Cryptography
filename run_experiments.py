import subprocess, sys
for script in ["run_test_vectors.py","run_security_analysis.py","run_round_analysis.py","run_benchmarks.py","generate_figures.py","generate_tables.py"]:
    print(f"\n==> {script}")
    subprocess.run([sys.executable,script],check=True)
