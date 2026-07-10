# Reproducibility Guide

Use Python 3.10 or newer. Install dependencies from the pinned requirement files, then run:

```bash
python verify_repository.py
python run_experiments.py
```

The pipeline uses fixed seeds and writes generated outputs to `results/`. The directory is intentionally generated at run time rather than committed as a third source folder.

Benchmark reports include raw nanosecond samples, mean, median, standard deviation, peak Python allocation and platform metadata. Repeat measurements on the same machine and avoid comparing results gathered under different power, thermal or CPU-governor settings.

For embedded reporting, compile `nlca/nlca_reference.c` with the exact target toolchain and record compiler version, flags, device model, clock frequency and optimization level.
