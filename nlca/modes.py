"""Experimental block-cipher modes for reproducible evaluation.

ECB is included only for primitive testing. CTR is the recommended streaming
mode in this research package. These modes do not provide authentication.
"""
from __future__ import annotations
from .cipher import NLCA
from .primitives import xor_bytes

def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    n = block_size - (len(data) % block_size)
    return data + bytes([n]) * n

def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    if not data or len(data) % block_size:
        raise ValueError("Invalid padded data length")
    n = data[-1]
    if n < 1 or n > block_size or data[-n:] != bytes([n]) * n:
        raise ValueError("Invalid PKCS#7 padding")
    return data[:-n]

def ecb_encrypt(data: bytes, cipher: NLCA) -> bytes:
    data = pkcs7_pad(data)
    return b"".join(cipher.encrypt_block(data[i:i+16]) for i in range(0, len(data), 16))

def ecb_decrypt(data: bytes, cipher: NLCA) -> bytes:
    if len(data) % 16:
        raise ValueError("Ciphertext length must be a multiple of 16")
    out = b"".join(cipher.decrypt_block(data[i:i+16]) for i in range(0, len(data), 16))
    return pkcs7_unpad(out)

def ctr_crypt(data: bytes, cipher: NLCA, nonce: bytes, initial_counter: int = 0) -> bytes:
    if len(nonce) != 8:
        raise ValueError("nonce must be exactly 8 bytes")
    out = bytearray()
    for block_index in range(0, len(data), 16):
        counter = initial_counter + block_index // 16
        if not 0 <= counter < 2**64:
            raise OverflowError("CTR counter exhausted")
        stream = cipher.encrypt_block(nonce + counter.to_bytes(8, "big"))
        block = data[block_index:block_index+16]
        out.extend(x ^ y for x, y in zip(block, stream))
    return bytes(out)
