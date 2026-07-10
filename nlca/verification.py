"""Repository-level verification helpers."""
from .constants import SBOX, INV_SBOX, PBOX128
from .cipher import encrypt_block, decrypt_block
from .primitives import permute_bits, substitute_nibbles
from .key_schedule import expand_key

def verify_core():
    assert len(set(SBOX)) == 16
    assert all(INV_SBOX[SBOX[i]] == i for i in range(16))
    assert sorted(PBOX128) == list(range(128))
    sample = bytes(range(16))
    assert permute_bits(permute_bits(sample), inverse=True) == sample
    assert substitute_nibbles(substitute_nibbles(sample), inverse=True) == sample
    key = bytes(range(16))
    ct = encrypt_block(sample, key)
    assert decrypt_block(ct, key) == sample
    assert expand_key(key) == expand_key(key)
    return True
