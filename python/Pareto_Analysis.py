"""
Pareto (80/20 Rule) Customer Revenue Concentration Analysis
Identifies how much revenue is concentrated in top customer accounts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data", "FactSales_Anonymized.csv")
OUTPUT_CSV_PATH = os.path.join(PROJECT_DIR, "outputs", "Pareto_Results.csv")
OUTPUT_IMG_PATH = os.path.join(PROJECT_DIR, "outputs", "Pareto_Chart.png")


def main():
    print("[PARETO] Running Pareto Revenue Concentration Analysis ...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing input data file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Step 1: Total revenue per customer, sorted highest to lowest
    cust_rev = (
        df.groupby("Customer")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Step 2: Calculate percentage shares
    cust_rev["Revenue_%"] = (cust_rev["Revenue"] / cust_rev["Revenue"].sum()) * 100
    cust_rev["Cumulative_%"] = cust_rev["Revenue_%"].cumsum()

    # Step 3: Add rankings
    cust_rev["Customer_Rank"] = range(1, len(cust_rev) + 1)
    cust_rev["Customer_Rank_%"] = (cust_rev["Customer_Rank"] / len(cust_rev)) * 100

    # Save details
    cust_rev.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"[PARETO] Detailed Pareto table exported to {OUTPUT_CSV_PATH}")

    # Step 4: Find exactly how many customers represent 80% of sales
    customers_to_80 = cust_rev[cust_rev["Cumulative_%"] <= 80]
    num_customers_80 = len(customers_to_80) + 1
    pct_of_customer_base = (num_customers_80 / len(cust_rev)) * 100

    print(f"\n--- Pareto Findings ---")
    print(
        f"  Total Customers: {len(cust_rev)}"
        f"\n  Customers needed to reach 80% revenue: {num_customers_80}"
        f"\n  That is {pct_of_customer_base:.1f}% of the total customer base."
    )

    # Step 5: Classic Pareto Chart
    fig, ax1 = plt.subplots(figsize=(12, 6))

    top_n = 20  # Plot top 20 for visual clarity
    plot_data = cust_rev.head(top_n)

    ax1.bar(plot_data["Customer"], plot_data["Revenue"], color="#4C72B0")
    ax1.set_ylabel("Revenue")
    ax1.set_xlabel("Customer")
    ax1.tick_params(axis="x", rotation=75)

    ax2 = ax1.twinx()
    ax2.plot(
        plot_data["Customer"],
        plot_data["Cumulative_%"],
        color="#C44E52",
        marker="o",
        linewidth=2,
    )
    ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
    ax2.set_ylabel("Cumulative Revenue %")
    ax2.set_ylim(0, 110)

    plt.title(
        f"Customer Revenue Pareto Chart (Top {top_n} Accounts)\n"
        f"Top {pct_of_customer_base:.1f}% of Customer Base Drives 80% of Total Revenue"
    )
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG_PATH, dpi=150)
    plt.close()
    print(f"[PARETO] Pareto chart visualization saved to {OUTPUT_IMG_PATH}")


if __name__ == "__main__":
    main()
