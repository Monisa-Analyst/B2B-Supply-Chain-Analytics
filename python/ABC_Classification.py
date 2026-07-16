"""
ABC Product Classification Analysis
Categorizes products into A, B, and C classes based on revenue contribution thresholds.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data", "FactSales_Anonymized.csv")
OUTPUT_CSV_PATH = os.path.join(PROJECT_DIR, "outputs", "ABC_Results.csv")
OUTPUT_IMG_PATH = os.path.join(PROJECT_DIR, "outputs", "ABC_Classification.png")


def main():
    print("[ABC] Running ABC Classification Analysis ...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing input data file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Step 1: Total revenue per product, sorted highest to lowest
    prod_rev = (
        df.groupby("Products")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Step 2: Calculate percentage shares
    prod_rev["Revenue_%"] = (prod_rev["Revenue"] / prod_rev["Revenue"].sum()) * 100
    prod_rev["Cumulative_%"] = prod_rev["Revenue_%"].cumsum()

    # Step 3: Classify into A, B, C tiers based on standard cumulative-% cutoffs
    # A: Top 70% of revenue, B: Next 20% (up to 90%), C: Bottom 10% (90% to 100%)
    def classify_abc(cum_pct):
        if cum_pct <= 70:
            return "A"
        elif cum_pct <= 90:
            return "B"
        else:
            return "C"

    prod_rev["ABC_Class"] = prod_rev["Cumulative_%"].apply(classify_abc)

    # Save details
    prod_rev.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"[ABC] Detailed ABC classification table exported to {OUTPUT_CSV_PATH}")

    # Generate class-level summary
    abc_summary = prod_rev.groupby("ABC_Class").agg(
        Products=("Products", "count"), Total_Revenue=("Revenue", "sum")
    )
    abc_summary["Product_Share_%"] = (
        abc_summary["Products"] / abc_summary["Products"].sum() * 100
    ).round(2)
    abc_summary["Revenue_Share_%"] = (
        abc_summary["Total_Revenue"] / abc_summary["Total_Revenue"].sum() * 100
    ).round(2)

    print("\n--- ABC Summary ---")
    print(abc_summary)

    # Step 4: Visualize product count share vs revenue share by ABC class
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(abc_summary))
    width = 0.35

    ax.bar(
        x - width / 2,
        abc_summary["Product_Share_%"],
        width,
        label="Share of Products (%)",
        color="#4C72B0",
    )
    ax.bar(
        x + width / 2,
        abc_summary["Revenue_Share_%"],
        width,
        label="Share of Revenue (%)",
        color="#55A868",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(abc_summary.index)
    ax.set_ylabel("Percentage (%)")
    ax.set_title("ABC Classification: Product Share vs Revenue Share")
    ax.legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_IMG_PATH, dpi=150)
    plt.close()
    print(f"[ABC] ABC classification visualization saved to {OUTPUT_IMG_PATH}")


if __name__ == "__main__":
    main()
