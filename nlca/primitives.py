"""Low-level reversible operations used by NLCA."""
from __future__ import annotations
from .constants import (
    BLOCK_SIZE_BYTES, SBOX, INV_SBOX, PBOX128, INV_PBOX128,
    P_TABLE, Q_TABLE
)

def require_block(value: bytes, name: str = "block") -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes-like")
    value = bytes(value)
    if len(value) != BLOCK_SIZE_BYTES:
        raise ValueError(f"{name} must be exactly {BLOCK_SIZE_BYTES} bytes")
    return value

def xor_bytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("XOR operands must have equal length")
    return bytes(x ^ y for x, y in zip(a, b))

def substitute_nibbles(state: bytes, inverse: bool = False) -> bytes:
    table = INV_SBOX if inverse else SBOX
    return bytes((table[b >> 4] << 4) | table[b & 0x0F] for b in state)

def permute_bits(state: bytes, inverse: bool = False) -> bytes:
    state = require_block(state)
    mapping = INV_PBOX128 if inverse else PBOX128
    out = [0] * 128
    for src in range(128):
        bit = (state[src // 8] >> (7 - (src % 8))) & 1
        dst = mapping[src]
        out[dst] = bit
    result = bytearray(16)
    for idx, bit in enumerate(out):
        result[idx // 8] |= bit << (7 - (idx % 8))
    return bytes(result)

def rotl128(value: bytes, shift: int) -> bytes:
    value = require_block(value)
    n = int.from_bytes(value, "big")
    shift %= 128
    mask = (1 << 128) - 1
    return (((n << shift) & mask) | (n >> (128 - shift))).to_bytes(16, "big")

def rotr128(value: bytes, shift: int) -> bytes:
    return rotl128(value, -shift)

def rotate_bytes_left(state: bytes, count: int) -> bytes:
    count %= len(state)
    return state[count:] + state[:count]

def rotate_bytes_right(state: bytes, count: int) -> bytes:
    count %= len(state)
    return state[-count:] + state[:-count] if count else state

def diffusion_layer(state: bytes, round_index: int) -> bytes:
    """Reversible lightweight diffusion using XOR coupling and byte rotation."""
    state = require_block(state)
    r = (1, 3, 5, 7, 2, 4, 6)[round_index % 7]
    x = bytearray(state)
    # Triangular XOR transformation, reversible in reverse order.
    for i in range(1, 16):
        x[i] ^= x[i - 1]
    x = bytearray(rotate_bytes_left(bytes(x), r))
    return bytes(x)

def inverse_diffusion_layer(state: bytes, round_index: int) -> bytes:
    r = (1, 3, 5, 7, 2, 4, 6)[round_index % 7]
    x = bytearray(rotate_bytes_right(require_block(state), r))
    for i in range(15, 0, -1):
        x[i] ^= x[i - 1]
    return bytes(x)

def f_function(word16: int) -> int:
    if not 0 <= word16 <= 0xFFFF:
        raise ValueError("f-function input must be a 16-bit integer")
    left = (word16 >> 8) & 0xFF
    right = word16 & 0xFF
    a = P_TABLE[left]
    b = Q_TABLE[right]
    return ((a ^ b) << 8) | ((P_TABLE[right] ^ Q_TABLE[left]) & 0xFF)

def hamming_distance(a: bytes, b: bytes) -> int:
    if len(a) != len(b):
        raise ValueError("Inputs must have equal length")
    return sum((x ^ y).bit_count() for x, y in zip(a, b))
