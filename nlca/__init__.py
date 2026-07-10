"""Reference implementation of the Novel Lightweight Cryptographic Algorithm (NLCA).

NLCA is treated here as an experimental 128-bit substitution-permutation network.
It is not a standardized or production-approved cryptographic primitive.
"""
from .cipher import NLCA, encrypt_block, decrypt_block
from .key_schedule import expand_key

__all__ = ["NLCA", "encrypt_block", "decrypt_block", "expand_key"]
__version__ = "1.0.0"
