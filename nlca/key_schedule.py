"""Deterministic, round-separated key schedule for NLCA."""
from __future__ import annotations
from .constants import KEY_SIZE_BYTES, ROUND_CONSTANTS, KEY_ROTATIONS
from .primitives import require_block, rotl128, substitute_nibbles, permute_bits, xor_bytes, f_function

def _f_mix(key: bytes) -> bytes:
    out = bytearray()
    for i in range(0, 16, 2):
        word = (key[i] << 8) | key[i + 1]
        out.extend(f_function(word).to_bytes(2, "big"))
    return bytes(out)

def expand_key(master_key: bytes, rounds: int = 5) -> list[bytes]:
    master_key = require_block(master_key, "master_key")
    if rounds < 1 or rounds > len(ROUND_CONSTANTS):
        raise ValueError(f"rounds must be in 1..{len(ROUND_CONSTANTS)}")
    state = master_key
    keys = []
    for r in range(rounds):
        state = rotl128(state, KEY_ROTATIONS[r])
        state = substitute_nibbles(state)
        state = permute_bits(state)
        state = xor_bytes(state, _f_mix(state))
        state = xor_bytes(state, ROUND_CONSTANTS[r])
        keys.append(state)
    return keys
