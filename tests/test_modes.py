from nlca.cipher import NLCA
from nlca.modes import ecb_encrypt, ecb_decrypt, ctr_crypt

def test_modes_roundtrip():
    cipher = NLCA(bytes(range(16)))
    data = b"reproducible IoT payload" * 11
    assert ecb_decrypt(ecb_encrypt(data, cipher), cipher) == data
    nonce = b"NLCA2026"
    ct = ctr_crypt(data, cipher, nonce)
    assert ctr_crypt(ct, cipher, nonce) == data
