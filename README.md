# NLCA IoT Cryptography

This repository contains a reproducible reference implementation and evaluation package for the experimental Novel Lightweight Cryptographic Algorithm (NLCA) described in the manuscript **Cloud-Based IoT Data Protection Using Lightweight and Efficient Cryptographic Methods**.

## Scientific scope

NLCA is implemented consistently as a 128-bit substitution–permutation network with a 128-bit key, a deterministic round-separated key schedule, a 4-bit S-box, a fixed 128-bit permutation derived from the reported 16-entry mapping, and a reversible lightweight diffusion layer. The default profile uses five rounds because that is the configuration studied in the manuscript. The round count remains configurable so that reduced-round and extended-round behavior can be examined.

This code is a research reference. It is not a standardized, independently audited, or production-approved cipher. Avalanche behavior, entropy, DDT and LAT measurements are evidence, not formal proof of security.

## Repository structure

Only two folders are used:

- `nlca/` — implementation, analysis, benchmarking, visualization and C reference code
- `tests/` — automated tests and machine-readable test vectors

The root contains all experiment entry points and reproducibility documents.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Windows activation:

```powershell
.venv\Scripts\activate
```

## Verify the complete repository

```bash
python verify_repository.py
```

## Generate test vectors

```bash
python run_test_vectors.py
```

## Run security analysis

```bash
python run_security_analysis.py
python run_round_analysis.py
```

## Run performance benchmark

```bash
python run_benchmarks.py --size 1048576 --repetitions 30
```

## Generate figures and tables

```bash
python generate_figures.py
python generate_tables.py
```

## Run the complete pipeline

```bash
python run_experiments.py
```

## CLI example

```bash
python -m nlca.cli encrypt   --key 000102030405060708090a0b0c0d0e0f   --plaintext 00112233445566778899aabbccddeeff
```

## Result provenance

Every baseline entry is tagged as `measured_local`, `library_execution`, `official_test_vector`, `literature_reported`, or `not_available`. Missing implementations are never replaced with invented values.

## Hardware reporting

Python memory measurements describe the Python process and must not be presented as embedded RAM or ROM use. The C reference implementation is provided for compiled code-size and platform-specific measurements. Hardware claims should be reported only after execution on the named device.

## Responsible use

Do not use the primitive directly for sensitive production data. The included CTR and ECB wrappers are experimental. ECB is for primitive testing only. The package does not claim authenticated encryption.
