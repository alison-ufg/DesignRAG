from collections import Counter

import pandas as pd

# Reading the CSV with semicolon separator (standard for Excel/CSV exports)
df = pd.read_csv("team_responses.csv", sep=";")

dev_columns = ["Dev_1", "Dev_2", "Dev_3", "Dev_4"]
final_ground_truth = []

print("--- PROCESSING GROUND TRUTH ---\n")

for index, row in df.iterrows():
    query_id = row["Query_ID"]
    all_votes = []

    # Collecting and cleaning votes
    for dev in dev_columns:
        # Get string, remove spaces, and split by comma
        votes_string = str(row[dev]).replace(", ", ",").split(",")
        # Strip whitespace and ignore empty strings (handles trailing commas)
        clean_votes = [
            vote.strip()
            for vote in votes_string
            if vote.strip() and vote.strip() != "nan"
        ]
        all_votes.extend(clean_votes)

    # Count frequencies
    vote_counts = Counter(all_votes)

    # Threshold: minimum of 2 votes, taking up to the 5 most frequent components
    approved_components = [
        comp for comp, count in vote_counts.most_common(207) if count >= 2
    ]

    final_ground_truth.append(
        {"Query_ID": query_id, "Official_Ground_Truth": ", ".join(approved_components)}
    )

df_result = pd.DataFrame(final_ground_truth)
df_result.to_csv("result_consolidated_ground_truth.csv", index=False)

print("Final Ground Truth Preview:")
print(df_result.head(30).to_string(index=False))
print("\n[+] 'result_consolidated_ground_truth.csv' generated successfully!")
