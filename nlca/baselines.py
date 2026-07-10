"""Baseline metadata and provenance controls.

The module intentionally does not fabricate measurements. Optional algorithms
are benchmarked only when a compatible local implementation is installed.
"""
BASELINES = {
    "AES-128": {"category": "standard block cipher", "provenance": "library_execution"},
    "PRESENT": {"category": "lightweight block cipher", "provenance": "not_available"},
    "GIFT-128": {"category": "lightweight block cipher", "provenance": "not_available"},
    "SKINNY-128": {"category": "lightweight block cipher", "provenance": "not_available"},
    "SIMON-128": {"category": "lightweight block cipher", "provenance": "not_available"},
    "SPECK-128": {"category": "lightweight block cipher", "provenance": "not_available"},
    "ASCON": {"category": "authenticated encryption", "provenance": "not_available"},
    "NLCA": {"category": "experimental SP-network", "provenance": "measured_local"},
}

def baseline_manifest():
    return BASELINES.copy()

def aes_encryptor(key: bytes):
    try:
        from Crypto.Cipher import AES
    except ImportError as exc:
        raise RuntimeError("Install pycryptodome to benchmark AES") from exc
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt
