import numpy as np
import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa

# Reading the CSV with semicolon separator
# Note: Ensure your local file is named 'team_responses.csv' or change this back
df = pd.read_csv("team_responses.csv", sep=";")
dev_columns = ["Dev_1", "Dev_2", "Dev_3", "Dev_4"]

print("--- CALCULATING AGREEMENT (FLEISS' KAPPA) ---\n")

# 1. Discover all unique components cited in the entire file
all_cited_components = set()
for index, row in df.iterrows():
    for dev in dev_columns:
        votes = [
            v.strip()
            for v in str(row[dev]).replace(", ", ",").split(",")
            if v.strip() and v.strip() != "nan"
        ]
        all_cited_components.update(votes)

unique_components = list(all_cited_components)

# 2. Build the agreement matrix
kappa_matrix = []

for index, row in df.iterrows():
    votes_per_dev = []
    for dev in dev_columns:
        votes = [
            v.strip()
            for v in str(row[dev]).replace(", ", ",").split(",")
            if v.strip() and v.strip() != "nan"
        ]
        votes_per_dev.append(votes)

    for comp in unique_components:
        yes_votes = sum(1 for dev_votes in votes_per_dev if comp in dev_votes)
        no_votes = 4 - yes_votes

        # Only add if the component was considered in this specific query
        if yes_votes > 0:
            kappa_matrix.append([no_votes, yes_votes])

# 3. Calculate Fleiss' Kappa
kappa_matrix_np = np.array(kappa_matrix)
kappa_score = fleiss_kappa(kappa_matrix_np, method="fleiss")

print(f"Fleiss' Kappa Score: {kappa_score:.4f}")

if kappa_score <= 0.60:
    print("Interpretation: Moderate Agreement")
elif kappa_score <= 0.80:
    print("Interpretation: Substantial Agreement (EXCELLENT)")
else:
    print("Interpretation: Almost Perfect Agreement (EXCELLENT)")
