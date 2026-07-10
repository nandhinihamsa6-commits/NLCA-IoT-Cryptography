"""Cryptanalytic and statistical evaluation utilities."""
from __future__ import annotations
import math, random
from collections import Counter
from .constants import SBOX
from .cipher import encrypt_block
from .primitives import hamming_distance

def difference_distribution_table(sbox=SBOX):
    n = len(sbox)
    table = [[0] * n for _ in range(n)]
    for dx in range(n):
        for x in range(n):
            table[dx][sbox[x] ^ sbox[x ^ dx]] += 1
    return table

def linear_approximation_table(sbox=SBOX):
    n = len(sbox)
    bits = int(math.log2(n))
    table = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            count = 0
            for x in range(n):
                lhs = (a & x).bit_count() & 1
                rhs = (b & sbox[x]).bit_count() & 1
                count += lhs == rhs
            table[a][b] = count - n // 2
    return table

def sbox_metrics(sbox=SBOX):
    ddt = difference_distribution_table(sbox)
    lat = linear_approximation_table(sbox)
    max_diff = max(max(row) for row in ddt[1:])
    max_bias = max(abs(v) for a, row in enumerate(lat) for b, v in enumerate(row) if not (a == 0 and b == 0))
    fixed = [x for x, y in enumerate(sbox) if x == y]
    opposite = [x for x, y in enumerate(sbox) if y == (x ^ 0xF)]
    nonlinearities = []
    for out_mask in range(1, 16):
        max_walsh = 0
        for in_mask in range(16):
            walsh = 0
            for x in range(16):
                parity = ((in_mask & x).bit_count() ^ (out_mask & sbox[x]).bit_count()) & 1
                walsh += 1 if parity == 0 else -1
            max_walsh = max(max_walsh, abs(walsh))
        nonlinearities.append(8 - max_walsh // 2)
    return {
        "bijective": len(set(sbox)) == len(sbox),
        "differential_uniformity": max_diff,
        "maximum_differential_probability": max_diff / 16,
        "maximum_linear_bias": max_bias / 16,
        "component_nonlinearity_min": min(nonlinearities),
        "component_nonlinearity_values": nonlinearities,
        "fixed_points": fixed,
        "opposite_fixed_points": opposite,
    }

def avalanche_profile(key: bytes, plaintext: bytes, rounds: int = 5, flip_key: bool = False):
    base = encrypt_block(plaintext, key, rounds)
    distances = []
    for bit in range(128):
        if flip_key:
            changed = bytearray(key)
            changed[bit // 8] ^= 1 << (7 - bit % 8)
            candidate = encrypt_block(plaintext, bytes(changed), rounds)
        else:
            changed = bytearray(plaintext)
            changed[bit // 8] ^= 1 << (7 - bit % 8)
            candidate = encrypt_block(bytes(changed), key, rounds)
        distances.append(hamming_distance(base, candidate))
    return {
        "distances": distances,
        "mean_bits_changed": sum(distances) / len(distances),
        "mean_percentage": 100 * sum(distances) / (len(distances) * 128),
        "minimum": min(distances),
        "maximum": max(distances),
    }

def round_avalanche(key: bytes, plaintext: bytes, max_rounds: int = 12):
    return [
        {"rounds": r, **avalanche_profile(key, plaintext, r)}
        for r in range(1, max_rounds + 1)
    ]

def byte_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())

def serial_correlation(data: bytes) -> float:
    if len(data) < 2:
        return 0.0
    x = list(data[:-1])
    y = list(data[1:])
    mx, my = sum(x)/len(x), sum(y)/len(y)
    num = sum((a-mx)*(b-my) for a,b in zip(x,y))
    denx = sum((a-mx)**2 for a in x)
    deny = sum((b-my)**2 for b in y)
    return num / math.sqrt(denx*deny) if denx and deny else 0.0

def reduced_round_report(key: bytes, plaintext: bytes, max_rounds: int = 12):
    rows = []
    for r in range(1, max_rounds + 1):
        av = avalanche_profile(key, plaintext, r)
        rows.append({
            "rounds": r,
            "mean_percentage": av["mean_percentage"],
            "minimum_bits_changed": av["minimum"],
            "maximum_bits_changed": av["maximum"],
        })
    return rows
