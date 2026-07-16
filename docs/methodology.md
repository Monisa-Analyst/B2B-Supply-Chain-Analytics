# Methodology

This document outlines the data engineering pipeline, analytical calculations, and star schema modeling implemented in this project.

---

## 1. Data Cleaning and Preparation

The raw sales register exported from Tally ERP was processed as follows:
* **Filtering**: Extra total lines, header rows, and metadata lines from the ERP ledger format were removed.
* **Schema Definition**: The data was structured into standard tabular columns: `Date`, `Customer`, `Products`, `Quantity`, `Rate`, and `Value ( Quantity * Rate )`.
* **Anonymization**: Real customer corporate identities were mapped to Customer aliases (Customer A, B, C...) and real part numbers mapped to Product SKUs (Product 001, 002, 003...).
* **Value Scaling**: All rates were scaled by a factor of 1.37 to protect financial confidentiality while maintaining original percentage trends and rankings.

---

## 2. Power BI Data Modeling

The data model utilizes a Star Schema configuration to optimize DAX query performance:
* **Fact Table**: `FactSales` (Date, Customer, Products, Quantity, Rate, Value).
* **Dimension Tables**: 
  * `DimCustomer`: Handles customer region and credit details.
  * `DimProduct`: Handles product categories and unit weight.
  * `DimCalendar`: An automated calendar table supporting monthly and yearly time-intelligence trends.

---

## 3. Python Analysis Framework

### RFM Segmentation
Scoring customers on:
* **Recency**: Days since the last transaction date.
* **Frequency**: Count of unique transaction dates.
* **Monetary**: Sum of value.
Quartile scoring was applied to segment accounts.

### Pareto (80/20) Analysis
Arranges customer revenue contributions in descending order to plot cumulative percentage lines and locate the 80% contribution threshold.

### ABC Product Classification
Tiers products by cumulative revenue shares:
* Class A: Top 70% of total revenue.
* Class B: Next 20% of revenue.
* Class C: Bottom 10% of revenue.

### Cohort Retention Analysis
Constructs a monthly pivot table of unique buyers offset from their first purchase month to monitor buyer recurrence patterns.
