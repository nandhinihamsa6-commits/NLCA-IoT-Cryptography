import json
from pathlib import Path
from nlca.security_analysis import difference_distribution_table, linear_approximation_table, sbox_metrics, avalanche_profile, reduced_round_report

def main():
    out = Path("results")
    out.mkdir(exist_ok=True)
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    report = {
        "sbox_metrics": sbox_metrics(),
        "plaintext_avalanche": avalanche_profile(key, pt),
        "key_avalanche": avalanche_profile(key, pt, flip_key=True),
        "round_analysis": reduced_round_report(key, pt, 12),
    }
    (out/"security_report.json").write_text(json.dumps(report, indent=2))
    (out/"ddt.json").write_text(json.dumps(difference_distribution_table(), indent=2))
    (out/"lat.json").write_text(json.dumps(linear_approximation_table(), indent=2))
    print("Wrote results/security_report.json, ddt.json and lat.json")

if __name__ == "__main__":
    main()
