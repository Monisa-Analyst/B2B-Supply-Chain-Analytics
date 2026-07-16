"""
Data Anonymization Script
Reads the raw FactSales.csv, replaces all customer and product names with
generic labels, and applies a consistent revenue multiplier so that rankings,
Pareto percentages, ABC classifications, and RFM segments remain identical.
"""

import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

RAW_DATA_PATH = r"D:\Manufacturing Sales Analytics\FactSales.csv"
OUTPUT_PATH = os.path.join(PROJECT_DIR, "data", "FactSales_Anonymized.csv")
CUST_MAP_PATH = os.path.join(SCRIPT_DIR, "customer_mapping.csv")
PROD_MAP_PATH = os.path.join(SCRIPT_DIR, "product_mapping.csv")

REVENUE_MULTIPLIER = 1.37


def main():
    print("[ANONYMIZE] Reading raw FactSales.csv ...")
    df = pd.read_csv(RAW_DATA_PATH)

    df = df.rename(columns={"Value ( Quantity * Rate )": "Revenue"})

    # --- Customer mapping (ranked by total revenue so labels are stable) ---
    cust_rev = (
        df.groupby("Customer")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    cust_rev["Anonymized"] = [
        f"Customer {chr(65 + i)}" if i < 26 else f"Customer {i + 1}"
        for i in range(len(cust_rev))
    ]
    cust_map = dict(zip(cust_rev["Customer"], cust_rev["Anonymized"]))

    # --- Product mapping (ranked by total revenue) ---
    prod_rev = (
        df.groupby("Products")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    prod_rev["Anonymized"] = [f"Product {i + 1:03d}" for i in range(len(prod_rev))]
    prod_map = dict(zip(prod_rev["Products"], prod_rev["Anonymized"]))

    # --- Apply mappings ---
    df["Customer"] = df["Customer"].map(cust_map)
    df["Products"] = df["Products"].map(prod_map)

    # --- Scale revenue values ---
    df["Rate"] = (df["Rate"] * REVENUE_MULTIPLIER).round(2)
    df["Revenue"] = (df["Quantity"] * df["Rate"]).round(2)

    # --- Export ---
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[ANONYMIZE] Wrote anonymized data to {OUTPUT_PATH}")
    print(f"[ANONYMIZE]   Rows: {len(df)}")
    print(f"[ANONYMIZE]   Customers: {df['Customer'].nunique()}")
    print(f"[ANONYMIZE]   Products: {df['Products'].nunique()}")

    # Save mappings locally (never upload these)
    cust_rev[["Customer", "Anonymized"]].to_csv(CUST_MAP_PATH, index=False)
    prod_rev[["Products", "Anonymized"]].to_csv(PROD_MAP_PATH, index=False)
    print(f"[ANONYMIZE] Mapping files saved (DO NOT UPLOAD):")
    print(f"  - {CUST_MAP_PATH}")
    print(f"  - {PROD_MAP_PATH}")

    # --- Verification ---
    print("\n[VERIFY] Checking for any remaining real names ...")
    raw = pd.read_csv(RAW_DATA_PATH)
    real_customers = set(raw["Customer"].unique())
    real_products = set(raw["Products"].unique())

    anon = pd.read_csv(OUTPUT_PATH)
    leaked_custs = real_customers.intersection(set(anon["Customer"].unique()))
    leaked_prods = real_products.intersection(set(anon["Products"].unique()))

    if leaked_custs:
        print(f"  WARNING: Real customer names found: {leaked_custs}")
    else:
        print("  OK: No real customer names in anonymized file.")

    if leaked_prods:
        print(f"  WARNING: Real product names found: {leaked_prods}")
    else:
        print("  OK: No real product names in anonymized file.")

    print("[ANONYMIZE] Done.")


if __name__ == "__main__":
    main()
