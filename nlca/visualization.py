"""Publication-ready scientific plots generated from measured data."""
from pathlib import Path
import json
import matplotlib.pyplot as plt

def plot_round_avalanche(rows, output_path):
    rounds = [r["rounds"] for r in rows]
    values = [r["mean_percentage"] for r in rows]
    plt.figure(figsize=(7, 4.5))
    plt.plot(rounds, values, marker="o")
    plt.axhline(50, linestyle="--", linewidth=1)
    plt.xlabel("Number of rounds")
    plt.ylabel("Mean changed ciphertext bits (%)")
    plt.title("NLCA avalanche convergence by round")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_matrix(matrix, title, output_path):
    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, aspect="auto")
    plt.colorbar()
    plt.xlabel("Output difference or mask")
    plt.ylabel("Input difference or mask")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
