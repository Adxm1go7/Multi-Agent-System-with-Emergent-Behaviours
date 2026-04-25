# analyse.py
# Run after experiments.py to get summary statistics and plots.
# pip install pandas matplotlib seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("results.csv")

print("=== Summary ===")
print(f"Total runs:    {len(df)}")
print(f"Converged:     {df['converged'].sum()} ({df['converged'].mean()*100:.1f}%)")
print(f"Mean variance: {df['final_variance'].mean():.4f}")
print()

# ── Plot 1: Convergence step vs epsilon, grouped by opinion type ───────────
fig, ax = plt.subplots(figsize=(10, 5))
for opinion_type, group in df.groupby("opinion_type"):
    means = group.groupby("convince_range")["convergence_step"].mean()
    ax.plot(means.index, means.values, marker="o", label=opinion_type)
ax.set_xlabel("Confidence Threshold (ε)")
ax.set_ylabel("Mean Convergence Step")
ax.set_title("Convergence Speed vs Confidence Threshold")
ax.legend()
plt.tight_layout()
plt.savefig("convergence_vs_epsilon.png", dpi=150)
print("Saved convergence_vs_epsilon.png")

# ── Plot 2: Heatmap of final variance (epsilon x converge_mult) ───────────
pivot = df[df["opinion_type"] == "continuous"].pivot_table(
    values="final_variance",
    index="converge_mult",
    columns="convince_range",
    aggfunc="mean",
)
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt=".3f", cmap="YlOrRd_r", ax=ax)
ax.set_title("Mean Final Variance (continuous mode)\nε × μ parameter space")
ax.set_xlabel("Confidence Threshold (ε)")
ax.set_ylabel("Convergence Multiplier (μ)")
plt.tight_layout()
plt.savefig("variance_heatmap.png", dpi=150)
print("Saved variance_heatmap.png")

# ── Plot 3: Effect of stubborn agents on convergence ──────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
for stub_frac, group in df.groupby("stubborn_fraction"):
    means = group.groupby("convince_range")["convergence_step"].mean()
    ax.plot(means.index, means.values, marker="o", label=f"stubborn={stub_frac}")
ax.set_xlabel("Confidence Threshold (ε)")
ax.set_ylabel("Mean Convergence Step")
ax.set_title("Effect of Stubborn Agents on Convergence Speed")
ax.legend()
plt.tight_layout()
plt.savefig("stubborn_effect.png", dpi=150)
print("Saved stubborn_effect.png")

# ── Plot 4: Number of clusters by epsilon ─────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
for opinion_type, group in df.groupby("opinion_type"):
    means = group.groupby("convince_range")["n_clusters"].mean()
    ax.plot(means.index, means.values, marker="o", label=opinion_type)
ax.set_xlabel("Confidence Threshold (ε)")
ax.set_ylabel("Mean Number of Clusters")
ax.set_title("Opinion Fragmentation vs Confidence Threshold")
ax.legend()
plt.tight_layout()
plt.savefig("clusters_vs_epsilon.png", dpi=150)
print("Saved clusters_vs_epsilon.png")

plt.show()