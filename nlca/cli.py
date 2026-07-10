"""Command-line interface for NLCA."""
import argparse, json
from .cipher import encrypt_block, decrypt_block

def _hex16(value: str, name: str) -> bytes:
    try:
        raw = bytes.fromhex(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{name} must be hexadecimal") from exc
    if len(raw) != 16:
        raise argparse.ArgumentTypeError(f"{name} must encode exactly 16 bytes")
    return raw

def main():
    parser = argparse.ArgumentParser(description="NLCA experimental reference implementation")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("encrypt", "decrypt", "trace"):
        p = sub.add_parser(command)
        p.add_argument("--key", required=True)
        p.add_argument("--rounds", type=int, default=5)
        p.add_argument("--plaintext" if command != "decrypt" else "--ciphertext", required=True)
    args = parser.parse_args()
    key = _hex16(args.key, "key")
    if args.command in ("encrypt", "trace"):
        pt = _hex16(args.plaintext, "plaintext")
        result = encrypt_block(pt, key, args.rounds, trace=args.command == "trace")
    else:
        ct = _hex16(args.ciphertext, "ciphertext")
        result = decrypt_block(ct, key, args.rounds)
    if args.command == "trace":
        ct, trace = result
        print(json.dumps({"ciphertext": ct.hex(), "trace": trace}, indent=2))
    else:
        print(result.hex())

if __name__ == "__main__":
    main()
