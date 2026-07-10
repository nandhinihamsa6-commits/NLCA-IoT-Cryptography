from nlca.key_schedule import expand_key

def test_schedule_deterministic_and_sized():
    key = bytes(range(16))
    a = expand_key(key, 5)
    b = expand_key(key, 5)
    assert a == b
    assert len(a) == 5
    assert all(len(x) == 16 for x in a)
    assert len(set(a)) == 5
