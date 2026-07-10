"""Authoritative constants for the reproducible NLCA reference profile."""

BLOCK_SIZE_BYTES = 16
BLOCK_SIZE_BITS = 128
KEY_SIZE_BYTES = 16
DEFAULT_ROUNDS = 5
NIBBLE_COUNT = 32

# 4-bit S-box reported in the manuscript.
SBOX = (
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7,
)

def _inverse_table(table):
    inv = [0] * len(table)
    for i, value in enumerate(table):
        inv[value] = i
    return tuple(inv)

INV_SBOX = _inverse_table(SBOX)

# 16-bit base permutation from Table 2. Entry i gives the destination of input bit i.
PBOX16 = (4, 12, 8, 0, 9, 1, 13, 5, 2, 14, 6, 10, 7, 15, 3, 11)
INV_PBOX16 = _inverse_table(PBOX16)

# Formal extension to 128 bits: the 16-bit mapping is applied independently
# to each of eight contiguous 16-bit state slices.
PBOX128 = tuple(16 * group + PBOX16[i] for group in range(8) for i in range(16))
INV_PBOX128 = _inverse_table(PBOX128)

# Fixed 8-bit substitution tables used by the key-schedule f-function.
# These are generated once from the manuscript S-box and committed as constants.
P_TABLE = tuple(((SBOX[x >> 4] << 4) | SBOX[x & 0x0F]) for x in range(256))
Q_TABLE = tuple((((SBOX[(x & 0x0F)] << 4) | SBOX[x >> 4]) ^ 0xA5) for x in range(256))

# Rotations and explicit 128-bit round constants for up to twelve rounds.
KEY_ROTATIONS = (13, 29, 47, 61, 79, 97, 109, 7, 23, 41, 67, 101)
ROUND_CONSTANTS_HEX = (
    "9e3779b97f4a7c15f39cc0605cedc835",
    "3c6ef372fe94f82be73980c0b9db906a",
    "daa66d2c7ddf7431dbd641a115c9649f",
    "78dde6e5fd29f047cf73018173b720d4",
    "1715609f7c746c5dc30fc1e1d1a5ad09",
    "b54cda58fbbee873b6ac82422f94293e",
    "538454127b096489aa4942a28d82a573",
    "f1bbcdcbfa53e09f9de60302eb712ba8",
    "8ff34785799e5cb59182c363496fb7dd",
    "2e2ac13ef8e8d8cb852f83c3a75e3412",
    "cc623af8783354e1798c4444054cc047",
    "6a99b4b1f77dd0f76d2904a4633b3c7c",
)
ROUND_CONSTANTS = tuple(bytes.fromhex(x) for x in ROUND_CONSTANTS_HEX)

# Per-round byte rotation used by the reversible diffusion layer.
DIFFUSION_ROTATIONS = (1, 3, 5, 7, 2, 4, 6, 1, 5, 3, 7, 2)
