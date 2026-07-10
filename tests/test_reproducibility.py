from nlca.datasets import random_bytes, synthetic_iot_records

def test_seeded_data_reproducible():
    assert random_bytes(1024, 7) == random_bytes(1024, 7)
    assert synthetic_iot_records(10, 9) == synthetic_iot_records(10, 9)
