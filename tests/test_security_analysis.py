from nlca.security_analysis import difference_distribution_table, linear_approximation_table, sbox_metrics, avalanche_profile

def test_tables_and_metrics():
    ddt = difference_distribution_table()
    lat = linear_approximation_table()
    assert len(ddt) == 16 and all(len(r) == 16 for r in ddt)
    assert len(lat) == 16 and all(len(r) == 16 for r in lat)
    m = sbox_metrics()
    assert m["bijective"] is True
    assert 0 < m["maximum_differential_probability"] <= 1

def test_avalanche_shape():
    key = bytes(range(16))
    pt = bytes(range(16, 32))
    result = avalanche_profile(key, pt)
    assert len(result["distances"]) == 128
