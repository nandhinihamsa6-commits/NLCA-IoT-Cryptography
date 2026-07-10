"""Reproducible timing and memory measurements."""
from __future__ import annotations
import os, platform, statistics, sys, time, tracemalloc
from .cipher import NLCA

def environment_metadata():
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
    }

def benchmark_callable(func, payload: bytes, repetitions: int = 30, warmups: int = 5):
    if repetitions < 2:
        raise ValueError("repetitions must be at least 2")
    for _ in range(warmups):
        func(payload)
    samples = []
    tracemalloc.start()
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        func(payload)
        samples.append(time.perf_counter_ns() - start)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mean_ns = statistics.mean(samples)
    return {
        "samples_ns": samples,
        "mean_ns": mean_ns,
        "median_ns": statistics.median(samples),
        "stdev_ns": statistics.stdev(samples),
        "min_ns": min(samples),
        "max_ns": max(samples),
        "peak_python_bytes": peak,
    }

def benchmark_nlca(size_bytes: int = 1024 * 1024, repetitions: int = 30, seed: int = 2026):
    import random
    rng = random.Random(seed)
    key = bytes(rng.getrandbits(8) for _ in range(16))
    data = bytes(rng.getrandbits(8) for _ in range(size_bytes))
    cipher = NLCA(key)
    def encrypt_payload(payload):
        padded = payload + b"\x00" * ((16 - len(payload) % 16) % 16)
        return b"".join(cipher.encrypt_block(padded[i:i+16]) for i in range(0, len(padded), 16))
    result = benchmark_callable(encrypt_payload, data, repetitions)
    result["size_bytes"] = size_bytes
    result["throughput_mbps"] = (size_bytes * 8) / (result["mean_ns"] / 1e9) / 1e6
    result["environment"] = environment_metadata()
    result["seed"] = seed
    return result
