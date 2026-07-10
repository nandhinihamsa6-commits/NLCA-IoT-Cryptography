import ctypes, pathlib, subprocess, tempfile
import pytest
from nlca.cipher import encrypt_block

@pytest.mark.skipif(not pathlib.Path("/usr/bin/gcc").exists(), reason="gcc unavailable")
def test_python_c_equivalence():
    root = pathlib.Path(__file__).resolve().parents[1]
    src = root / "nlca" / "nlca_reference.c"
    with tempfile.TemporaryDirectory() as td:
        lib = pathlib.Path(td) / "libnlca.so"
        subprocess.run(["gcc","-shared","-fPIC","-O2",str(src),"-o",str(lib)],check=True)
        dll = ctypes.CDLL(str(lib))
        arr = ctypes.c_uint8 * 16
        key = bytes(range(16))
        pt = bytes(range(16,32))
        out = arr()
        dll.nlca_encrypt_block(arr(*pt), arr(*key), out)
        assert bytes(out) == encrypt_block(pt,key)
