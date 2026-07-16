# Data Privacy Audit

This document outlines the risk assessment and anonymization steps performed to ensure that no proprietary, confidential, or sensitive customer information is leaked when publishing the Manufacturing Sales and Customer Intelligence Platform project to public spaces.

---

## 1. Sensitive Information Identified

The raw data source consists of ledger records exported directly from Tally ERP. The following fields and identifiers were flagged as high-risk for leakage:

1. **Company Identity**: The raw export contained references to "Anand Engineering" (the manufacturing organization).
2. **Customer Names**: A total of 52 unique corporate entity names were listed in the raw sales ledger (e.g., "ALDICA TECHNOLOGIES PRIVATE LIMITED", "SUPRAJIT ENGINEERING LIMITED, UNIT-9", "TEKNIC EUCHNER ELECTRONICS PVT LTD"). These are real businesses whose purchase habits constitute proprietary commercial agreements.
3. **Product Names**: A total of 248 product names were listed, containing specific engineering part numbers and descriptions (e.g., "PRV BODY COMPONENT 47500010004", "ZINC SLEEVE SEL/102/592").
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

## 3. File Controls

* **FactSales.csv (Raw)**: Stored strictly in local scratch directory `D:\Manufacturing Sales Analytics\`. Excluded from the git repository using `.gitignore`.
* **Anonymization Mappings**: Customer and product mapping CSV files (`customer_mapping.csv`, `product_mapping.csv`) are stored locally in the `scripts/` directory and are explicitly ignored by `.gitignore`.
* **Power BI Cache**: Power BI files contain cached query data. The file `Manufacturing_Sales_Analytics_.pbix` copied to the repository must be refreshed with the anonymized CSV before public hosting to overwrite the old cache.
