"""Deterministic payload generation for reproducible experiments."""
import csv, io, json, random

def random_bytes(size: int, seed: int = 2026) -> bytes:
    rng = random.Random(seed)
    return bytes(rng.getrandbits(8) for _ in range(size))

def synthetic_iot_records(count: int = 1000, seed: int = 2026) -> bytes:
    rng = random.Random(seed)
    rows = []
    for i in range(count):
        rows.append({
            "device_id": f"sensor-{i % 25:02d}",
            "timestamp": 1767225600 + i,
            "temperature_c": round(rng.uniform(18, 42), 3),
            "humidity_pct": round(rng.uniform(20, 95), 3),
            "pressure_hpa": round(rng.uniform(980, 1040), 3),
            "status": "ok" if rng.random() > 0.03 else "alert",
        })
    return "\n".join(json.dumps(x, sort_keys=True) for x in rows).encode()
