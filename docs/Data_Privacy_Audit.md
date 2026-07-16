# Data Privacy Audit

This document outlines the risk assessment and anonymization steps performed to ensure that no proprietary, confidential, or sensitive customer information is leaked when publishing the Manufacturing Sales and Customer Intelligence Platform project to public spaces.

---

## 1. Sensitive Information Identified

The raw data source consists of ledger records exported directly from Tally ERP. The following fields and identifiers were flagged as high-risk for leakage:

1. **Company Identity**: The raw export contained references to the manufacturing organization.
2. **Customer Names**: A total of 52 unique corporate entity names were listed in the raw sales ledger. These are real businesses whose purchase habits constitute proprietary commercial agreements.
3. **Product Names**: A total of 248 product names were listed, containing specific engineering part numbers and descriptions.
4. **Absolute Financial Metrics**: Real purchase quantities, rates, and invoice totals reflecting the exact order values and sales volume of the company.

---

## 2. Anonymization and Masking Methodology

A python-based anonymization pipeline was executed to convert the raw ledger into a clean, safe dataset:

1. **Customer Masking**: Customer names were sorted by their total revenue contribution and mapped deterministically to generic aliases (`Customer A`, `Customer B`, `Customer C`, etc.).
2. **Product Masking**: Product names were sorted by their total revenue contribution and mapped to serialized aliases (`Product 001`, `Product 002`, `Product 003`, etc.).
3. **Revenue Scaling**: All rates were scaled by a consistent multiplier of `1.37`. This changes the absolute order values so that the company's real revenue figures cannot be reconstructed, while mathematically preserving:
   * Rank ordering of customers and products.
   * RFM customer segments and scoring boundaries.
   * Pareto 80/20 customer concentration ratios.
   * ABC classification categories and relative shares.
4. **Metadata Scrubbing**: Custom headers, local file paths, and author profiles were stripped from Python, SQL, and Markdown documentation.

---

## 3. File Controls and Git Ignored Patterns

To prevent the accidental publication of cached data or mapping logs, the repository utilizes the following safety controls:

* **Complete Dataset Exclusion**: The anonymized data (`FactSales.csv`) and output tables (`RFM_Output.csv`, `Pareto_Output.csv`, `ABC_Output.csv`, `Cohort_Output.csv`) are kept locally and are completely excluded from the Git tree via the `*.csv` rule in `.gitignore`.
* **Power BI Cache Exclusion**: Power BI `.pbix` files cache query data inside the file structure itself. To prevent data leaks, all `.pbix` files are strictly excluded from the Git tree via the `*.pbix` rule in `.gitignore` and are not hosted on public platforms.
* **Local Mappings**: Customer and product mapping CSV logs used in the pipeline are stored locally and are ignored by Git.
