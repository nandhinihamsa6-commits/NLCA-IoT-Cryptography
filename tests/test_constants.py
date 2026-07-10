from nlca.constants import SBOX, INV_SBOX, PBOX128, INV_PBOX128

def test_sbox_bijective():
    assert sorted(SBOX) == list(range(16))
    assert all(INV_SBOX[SBOX[x]] == x for x in range(16))

def test_pbox_bijective():
    assert sorted(PBOX128) == list(range(128))
    assert all(INV_PBOX128[PBOX128[x]] == x for x in range(128))
