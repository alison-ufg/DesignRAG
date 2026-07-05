import json


def calculate_and_print_averages(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        return

    print("=" * 40)
    print(" DESCRIPTIVE ANALYSIS (GLOBAL AVERAGES)")
    print("=" * 40)

    # Defined order for printing
    metric_order = ["P@1", "P@3", "P@5", "MRR"]

    # Order of models based on your article table
    model_order = [
        "FTS",
        "RAG",
        "G_2.5_F",
        "G_2.5_P",
        "G_3.0_P",
        "GPT_5_M",
        "GPT_5",
    ]

    for metric in metric_order:
        if metric not in data:
            continue

        print(f"\n--- Metric: {metric} ---")
        models = data[metric]

        for model in model_order:
            if model in models:
                values = models[model]
                average = sum(values) / len(values)
                print(f"{model:<12}: {average:.2f}")


if __name__ == "__main__":
    calculate_and_print_averages("metrics.json")
