"""Reversible NLCA block-cipher reference implementation."""
from __future__ import annotations
from dataclasses import dataclass
from .constants import DEFAULT_ROUNDS
from .primitives import (
    require_block, xor_bytes, substitute_nibbles, permute_bits,
    diffusion_layer, inverse_diffusion_layer
)
from .key_schedule import expand_key

def encrypt_block(plaintext: bytes, key: bytes, rounds: int = DEFAULT_ROUNDS, trace: bool = False):
    state = require_block(plaintext, "plaintext")
    round_keys = expand_key(key, rounds)
    traces = []
    for r, rk in enumerate(round_keys):
        state = xor_bytes(state, rk)
        state = substitute_nibbles(state)
        state = permute_bits(state)
        state = diffusion_layer(state, r)
        if trace:
            traces.append({"round": r + 1, "state": state.hex(), "round_key": rk.hex()})
    return (state, traces) if trace else state

def decrypt_block(ciphertext: bytes, key: bytes, rounds: int = DEFAULT_ROUNDS, trace: bool = False):
    state = require_block(ciphertext, "ciphertext")
    round_keys = expand_key(key, rounds)
    traces = []
    for r in range(rounds - 1, -1, -1):
        state = inverse_diffusion_layer(state, r)
        state = permute_bits(state, inverse=True)
        state = substitute_nibbles(state, inverse=True)
        state = xor_bytes(state, round_keys[r])
        if trace:
            traces.append({"round": r + 1, "state": state.hex(), "round_key": round_keys[r].hex()})
    return (state, traces) if trace else state

@dataclass(frozen=True)
class NLCA:
    key: bytes
    rounds: int = DEFAULT_ROUNDS

    def __post_init__(self):
        require_block(self.key, "key")
        expand_key(self.key, self.rounds)

    def encrypt_block(self, plaintext: bytes) -> bytes:
        return encrypt_block(plaintext, self.key, self.rounds)

    def decrypt_block(self, ciphertext: bytes) -> bytes:
        return decrypt_block(ciphertext, self.key, self.rounds)
