import random
from nlca.cipher import encrypt_block, decrypt_block

def test_known_vector():
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    ct = encrypt_block(pt, key)
    assert decrypt_block(ct, key) == pt

def test_random_roundtrips():
    rng = random.Random(2026)
    for rounds in range(1, 13):
        for _ in range(10):
            key = bytes(rng.getrandbits(8) for _ in range(16))
            pt = bytes(rng.getrandbits(8) for _ in range(16))
            assert decrypt_block(encrypt_block(pt, key, rounds), key, rounds) == pt
