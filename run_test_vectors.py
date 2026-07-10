import json
from pathlib import Path
from nlca.cipher import encrypt_block, decrypt_block
from nlca.key_schedule import expand_key

vectors=[]
for i in range(5):
    key=bytes((x+i)&255 for x in range(16))
    pt=bytes((0x11*x+3*i)&255 for x in range(16))
    ct=encrypt_block(pt,key)
    assert decrypt_block(ct,key)==pt
    vectors.append({"id":i+1,"key":key.hex(),"plaintext":pt.hex(),"ciphertext":ct.hex(),"round_keys":[x.hex() for x in expand_key(key)]})
Path("tests/test_vectors.json").write_text(json.dumps(vectors,indent=2))
print("Generated tests/test_vectors.json")
