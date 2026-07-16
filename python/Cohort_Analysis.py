"""
Cohort Retention Analysis
Evaluates customer retention patterns over time, calculating the percentage
of active customers in subsequent months following their first purchase.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data", "FactSales_Anonymized.csv")
OUTPUT_CSV_PATH = os.path.join(PROJECT_DIR, "outputs", "Cohort_Output.csv")
OUTPUT_IMG_PATH = os.path.join(PROJECT_DIR, "outputs", "Cohort_Heatmap.png")


def main():
    print("[COHORT] Running Cohort Retention Analysis ...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing input data file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")

    # Step 1: Assign transaction month and cohort (first purchase) month
    df["Transaction_Month"] = df["Date"].dt.to_period("M")
    df["Cohort_Month"] = (
        df.groupby("Customer")["Date"].transform("min").dt.to_period("M")
    )

    # Step 2: Calculate Cohort Index (months difference)
    def month_diff(row):
        return (
            (row["Transaction_Month"].year - row["Cohort_Month"].year) * 12
            + (row["Transaction_Month"].month - row["Cohort_Month"].month)
        )

    df["Cohort_Index"] = df.apply(month_diff, axis=1)

    # Step 3: Build cohort pivot table (distinct active customer count)
    cohort_data = (
        df.groupby(["Cohort_Month", "Cohort_Index"])["Customer"]
        .nunique()
        .reset_index()
    )
    cohort_counts = cohort_data.pivot(
        index="Cohort_Month", columns="Cohort_Index", values="Customer"
    )

    # Step 4: Convert counts to retention percentage rates
    cohort_size = cohort_counts.iloc[:, 0]
    retention_matrix = cohort_counts.divide(cohort_size, axis=0) * 100

    # Save retention matrix CSV (rounded to 1 decimal place)
    retention_matrix.round(1).to_csv(OUTPUT_CSV_PATH)
    print(f"[COHORT] Cohort retention matrix exported to {OUTPUT_CSV_PATH}")

    # Step 5: Visualize retention matrix as a heatmap
    fig, ax = plt.subplots(figsize=(14, 9))
    data = retention_matrix.values

    # Using YlGnBu color palette to match typical retention displays
    im = ax.imshow(data, cmap="YlGnBu", aspect="auto", vmin=0, vmax=100)

    ax.set_xticks(range(retention_matrix.shape[1]))
    ax.set_xticklabels(retention_matrix.columns)
    ax.set_yticks(range(retention_matrix.shape[0]))
    ax.set_yticklabels([str(p) for p in retention_matrix.index])

    ax.set_xlabel("Cohort Index (Months Since First Purchase)")
    ax.set_ylabel("Cohort Month (First Purchase Month)")
    ax.set_title("Customer Retention Heatmap (%)")

    # Annotate values inside each cell
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if not np.isnan(val):
                ax.text(
                    j,
                    i,
                    f"{val:.0f}",
                    ha="center",
                    va="center",
                    color="white" if val > 50 else "black",
                    fontsize=8,
                )

    fig.colorbar(im, ax=ax, label="Retention Rate (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG_PATH, dpi=150)
    plt.close()
    print(f"[COHORT] Cohort heatmap visualization saved to {OUTPUT_IMG_PATH}")


if __name__ == "__main__":
    main()
