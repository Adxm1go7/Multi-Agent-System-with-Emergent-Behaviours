# TO RUN (/from backend):
# python experiments.py

# Runs the model multiple times across a grid of parameters,
# Saves results to CSV

import csv
import time
import itertools
import numpy as np
from Model import OpinionDynamicsModel, OpinionScenario

# The script runs every combination (cartesian product)

SWEEP = {
    "interaction_mode": ["single", "all_hk", "all_weighted"],
    "convince_range":   [0.1, 0.2, 0.3, 0.5, 1.0],
    "converge_mult":    [0.1, 0.3, 0.5],
    "grid_length":      [10],
    "opinion_type":     ["continuous", "binary", "ternary"],
    "stubborn_fraction":[0.0, 0.1, 0.2],
}

# Fixed parameters (these dont vary across sweeps)
FIXED = {
    "bias":             0.5,
    "bias_strength":    0.0,
    "n_broadcasters":   0,
    "broadcast_opinion":1.0,
}

N_REPLICATIONS = 5    # how many runs per parameter combination
MAX_STEPS      = 500   # max steps per run before stopping
CONVERGENCE_THRESHOLD = 0.001  # variance below this = converged
OUTPUT_FILE    = "results.csv"


def run_simulation(params, seed):
    """
    Run one simulation with the given params and seed.
    Returns a dict of metrics for this run.
    """
    scenario = OpinionScenario(
        grid_length        = params["grid_length"],
        convince_range     = params["convince_range"],
        converge_mult      = params["converge_mult"],
        opinion_type       = params["opinion_type"],
        stubborn_fraction  = params["stubborn_fraction"],
        bias               = params["bias"],
        bias_strength      = params["bias_strength"],
        n_broadcasters     = params["n_broadcasters"],
        broadcast_opinion  = params["broadcast_opinion"],
        seed               = seed,
    )
    model = OpinionDynamicsModel(scenario=scenario)

    converged_at    = None   # step at which convergence was reached
    final_variance  = None
    final_mean      = None
    n_clusters      = None

    for step in range(MAX_STEPS):
        model.step()
        opinions = [a.opinion for a in model.agents]
        variance = float(np.var(opinions))

        if variance <= CONVERGENCE_THRESHOLD and converged_at is None:
            converged_at = step + 1
            break   # stop early once converged

    # Final state metrics
    opinions       = [a.opinion for a in model.agents]
    final_variance = float(np.var(opinions))
    final_mean     = float(np.mean(opinions))
    n_clusters     = count_clusters(opinions, threshold=0.05)
    polarisation   = float(np.mean([1 for o in opinions if o < 0.2 or o > 0.8])) / max(len(opinions), 1)

    return {
        # Input params
        **params,
        "seed":              seed,
        "replication":       seed,

        # Output metrics
        "converged":         converged_at is not None,
        "convergence_step":  converged_at if converged_at else MAX_STEPS,
        "final_variance":    round(final_variance, 6),
        "final_mean":        round(final_mean, 4),
        "n_clusters":        n_clusters,
        "polarisation":      round(polarisation, 4),
    }


def count_clusters(opinions, threshold=0.05):
    """
    Count distinct opinion clusters.
    Two opinions are in the same cluster if they are within
    threshold of each other.
    """
    if not opinions:
        return 0

    sorted_opinions = sorted(opinions)
    clusters        = 1
    for i in range(1, len(sorted_opinions)):
        if sorted_opinions[i] - sorted_opinions[i - 1] > threshold:
            clusters += 1
    return clusters


def run_sweep():
    keys   = list(SWEEP.keys())
    values = list(SWEEP.values())
    combinations = list(itertools.product(*values))

    total_runs = len(combinations) * N_REPLICATIONS
    print(f"Running {len(combinations)} parameter combinations × {N_REPLICATIONS} replications = {total_runs} total runs")
    print(f"Output: {OUTPUT_FILE}\n")

    # CSV columns = all param keys + all metric keys
    fieldnames = list(FIXED.keys()) + keys + [
        "seed", "replication",
        "converged", "convergence_step",
        "final_variance", "final_mean",
        "n_clusters", "polarisation",
    ]

    completed = 0
    start_time = time.time()

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for combo in combinations:
            # Build params dict for this combination
            params = {**FIXED, **dict(zip(keys, combo))}

            for rep in range(N_REPLICATIONS):
                seed = rep * 1000 + hash(str(combo)) % 1000
                seed = abs(seed) % 99999 

                try:
                    result = run_simulation(params, seed)
                    writer.writerow(result)
                    f.flush()   # write immediately so we don't lose results on crash
                except Exception as e:
                    print(f"  ERROR: {params} seed={seed}: {e}")

                completed += 1

                # Progress indicator
                elapsed  = time.time() - start_time
                per_run  = elapsed / completed
                remaining = (total_runs - completed) * per_run
                print(
                    f"  [{completed}/{total_runs}] "
                    f"ε={params['convince_range']} "
                    f"μ={params['converge_mult']} "
                    f"grid={params['grid_length']} "
                    f"type={params['opinion_type']} "
                    f"-> converged={result['converged']} "
                    f"at step={result['convergence_step']} "
                    f"ETA {remaining:.0f}s"
                )

    print(f"\nDone. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_sweep()