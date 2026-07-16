"""
RFM (Recency, Frequency, Monetary) Customer Segmentation Analysis
Identifies Champions, Loyal, At Risk, and Lost customer segments.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# Set paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data", "FactSales_Anonymized.csv")
OUTPUT_CSV_PATH = os.path.join(PROJECT_DIR, "outputs", "RFM_Results.csv")
OUTPUT_IMG_PATH = os.path.join(PROJECT_DIR, "outputs", "RFM_Segments.png")


def main():
    print("[RFM] Running RFM Segmentation Analysis ...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing input data file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")

    # Define snapshot date as 1 day after the latest transaction
    snapshot_date = df["Date"].max() + pd.Timedelta(days=1)
    print(f"[RFM] Reference snapshot date: {snapshot_date.date()}")

    # Aggregate R, F, M by Customer
    rfm = (
        df.groupby("Customer")
        .agg(
            Recency=("Date", lambda x: (snapshot_date - x.max()).days),
            Frequency=("Date", "nunique"),
            Monetary=("Revenue", "sum"),
        )
        .reset_index()
    )

    # Score R, F, M metrics on a scale of 1-4
    # Recency: lower days is better, so reverse the labels
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1]).astype(int)

    # For frequency, if we have duplicate bins, use rank(method='first') to assign quartiles fairly
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]
    ).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4]).astype(int)

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    # Business rules for segments
    def assign_segment(row):
        if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
            return "Champions"
        elif row["F_Score"] >= 3 and row["M_Score"] >= 3:
            return "Loyal Customers"
        elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
            return "At Risk"
        elif row["R_Score"] <= 2 and row["F_Score"] <= 2:
            return "Lost Customers"
        else:
            return "Potential / Others"

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)

    # Export individual customer segment scores
    rfm.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"[RFM] Customer-level segments exported to {OUTPUT_CSV_PATH}")

    # Generate segment-level aggregations
    segment_summary = (
        rfm.groupby("Segment")
        .agg(
            Customers=("Customer", "count"),
            Total_Revenue=("Monetary", "sum"),
            Avg_Recency_Days=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
        )
        .sort_values("Total_Revenue", ascending=False)
    )

    segment_summary["Revenue_Share_%"] = (
        segment_summary["Total_Revenue"] / segment_summary["Total_Revenue"].sum() * 100
    ).round(2)

    print("\n--- Segment Summary ---")
    print(segment_summary)

    # Plot customer segments count and revenue contribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    segment_summary["Customers"].plot(kind="bar", ax=axes[0], color="#4C72B0")
    axes[0].set_title("Customer Count by Segment")
    axes[0].set_ylabel("Customers")
    axes[0].set_xlabel("")
    axes[0].tick_params(axis="x", rotation=45)

    segment_summary["Total_Revenue"].plot(kind="bar", ax=axes[1], color="#55A868")
    axes[1].set_title("Revenue Contribution by Segment")
    axes[1].set_ylabel("Revenue")
    axes[1].set_xlabel("")
    axes[1].yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(OUTPUT_IMG_PATH, dpi=150)
    plt.close()
    print(f"[RFM] Segments visualization saved to {OUTPUT_IMG_PATH}")


if __name__ == "__main__":
    main()
