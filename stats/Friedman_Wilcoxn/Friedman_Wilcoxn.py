import json

import numpy as np
from scipy.stats import friedmanchisquare, wilcoxon
from statsmodels.stats.multitest import multipletests

# 1. Load data from external JSON file
json_filename = "mrr_results.json"
try:
    with open(json_filename, "r", encoding="utf-8") as f:
        raw_results = json.load(f)
except FileNotFoundError:
    print(
        f"Error: Could not find '{json_filename}'. Please ensure it is in the same directory."
    )
    exit(1)

# Convert lists to NumPy arrays dynamically
results = {model: np.array(scores) for model, scores in raw_results.items()}

# Getting only the arrays for the global test
data = list(results.values())

print("--- STEP 1: GLOBAL TEST (FRIEDMAN) ---")
stat_friedman, p_friedman = friedmanchisquare(*data)
print(f"Friedman Statistic: {stat_friedman:.3f}")
print(f"Global P-Value: {p_friedman:.5e}")

if p_friedman < 0.05:
    print(
        "\nConclusion: Significant difference found among models. Proceeding to pairwise comparisons.\n"
    )

    print("--- STEP 2: PAIRWISE COMPARISON (WILCOXON) ---")

    # Comparing all multimodal models against BOTH baselines (Pure RAG and FTS)
    baselines = ["FTS", "Pure_RAG"]
    multimodal_models = [
        "GPT_Mini",
        "Gemini_Flash",
        "GPT_Pro",
        "Gemini_Pro",
        "Gemini_3_Pro",
    ]

    comparisons = []
    raw_p_values = []
    w_stats = []

    # Running Wilcoxon for each pair
    for baseline in baselines:
        for model in multimodal_models:
            stat, p_val = wilcoxon(
                results[baseline], results[model], alternative="less"
            )
            comparisons.append(f"{model} vs {baseline}")
            w_stats.append(stat)
            raw_p_values.append(p_val)

    # CRITICAL STEP: Holm-Bonferroni correction for multiple comparisons
    reject_h0, corrected_p_values, _, _ = multipletests(
        raw_p_values, alpha=0.05, method="holm"
    )

    # Displaying formatted results
    print(
        f"{'Comparison':<25} | {'Stat W':<8} | {'Raw P-Val':<10} | {'Corrected P':<12} | {'Significant?':<15}"
    )
    print("-" * 80)

    for i in range(len(comparisons)):
        sig_str = "YES (Multimodal wins)" if reject_h0[i] else "NO"
        print(
            f"{comparisons[i]:<25} | {w_stats[i]:<8.1f} | {raw_p_values[i]:<10.5f} | {corrected_p_values[i]:<12.5f} | {sig_str}"
        )

else:
    print("No significant difference found among the models.")
