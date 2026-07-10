import json
from pathlib import Path
from nlca.security_analysis import difference_distribution_table, linear_approximation_table
from nlca.visualization import plot_round_avalanche, plot_matrix

out=Path("results"); out.mkdir(exist_ok=True)
rows=json.loads((out/"round_analysis.json").read_text()) if (out/"round_analysis.json").exists() else []
if rows:
    plot_round_avalanche(rows,out/"figure_round_avalanche.png")
plot_matrix(difference_distribution_table(),"NLCA S-box Difference Distribution Table",out/"figure_ddt.png")
plot_matrix(linear_approximation_table(),"NLCA S-box Linear Approximation Table",out/"figure_lat.png")
print("Figures generated in results/")
