# Manufacturing Sales & Customer Intelligence Platform

An end-to-end data analytics and business intelligence project transforming raw B2B manufacturing sales register data into customer and product intelligence. This project utilizes SQL and Python to analyze purchasing behavior, segment customer accounts, classify product inventory, and map revenue concentration risks.

---

## Project Overview

B2B manufacturing suppliers often struggle to extract actionable insights from traditional ERP ledgers. In this project, raw sales transaction ledger data exported from Tally ERP was cleaned, structured, and analyzed to support executive decisions.

The platform provides visibility into:
1. Customer Segments: Scoring customers on Recency, Frequency, and Monetary (RFM) metrics to group them into actionable business tiers (Champions, Loyal, At Risk, Lost).
2. Revenue Concentration: Applying Pareto (80/20) analysis to measure key customer dependencies.
3. Product Classification: Categorizing inventory using ABC classification based on revenue contribution.
4. Retention Metrics: Analyzing cohort retention rates to evaluate customer lifecycle patterns.

---

## Repository Structure

To ensure complete data privacy and prevent any accidental leakage of proprietary business transaction data, all raw data tables, CSV exports, and Power BI caching files (.pbix) are strictly excluded from the Git tree. Only the clean analytical code and output plots are tracked.

```
Manufacturing-Sales-Customer-Intelligence-Platform/
├── sql/
│   ├── 01_Revenue_Analysis.sql          # Monthly sales aggregates and threshold queries
│   ├── 02_Customer_Analysis.sql         # Customer revenue rankings and share percentages
│   ├── 03_Product_Analysis.sql          # Product sales volume and quantity rankings
│   └── 04_Growth_Analysis.sql           # Period-over-period growth and cumulative trends
├── python/
│   └── Manufacturing_Sales_Analytics.ipynb # Main Python notebook for RFM, Pareto, ABC, and Cohort analysis
├── outputs/
│   ├── RFM_Segments.png                 # Segment customer count & revenue contribution plot
│   ├── Pareto_Chart.png                 # Dual-axis Pareto chart
│   └── Cohort_Heatmap.png               # Customer retention rate monthly heatmap
├── scripts/
│   └── anonymize_data.py                # Standalone script to clean and mask raw data locally
└── docs/
    ├── Data_Privacy_Audit.md            # Privacy policies and anonymization details
    └── GitHub_Publication_Checklist.md   # Step-by-step verification checklist
```

---

## Dataset Description

The analysis covers 2.5 years of transactional data (April 2024 to June 2026) containing 1,839 sales line items. The schema is modeled as follows:

* Date: Transaction timestamp (DD-MMM-YY format).
* Customer: Corporate buyer identifier.
* Products: Product SKU identifier.
* Quantity: Number of units sold.
* Rate: Price per unit.
* Revenue: Total transaction value (Quantity * Rate).

---

## Data Engineering and Modeling

1. Extraction and Cleaning: The raw ERP export was cleaned in Excel and Power Query. Extraneous header blocks, empty rows, and total lines were filtered. Corporate buyer names and physical parts were mapped to standardized, anonymized labels.
2. Data Scaling: Rate and revenue figures were scaled by a factor of 1.37 in local environments. This prevents the reconstruction of the company's real financial statements while preserving all mathematical rankings, proportions, and analytics outputs.

---

## SQL Analysis

The sql/ directory contains standard queries used to extract key operational reports from the data:
* Revenue Performance: Monthly revenue aggregates, running totals, and target threshold filters (identifying periods falling below targets).
* Customer Performance: Absolute sales rankings and cumulative revenue shares using window functions (RANK() OVER and SUM() OVER).
* Product Performance: SKU sales rankings by total units sold and net revenue generated.
* Growth Metrics: Month-over-month (MoM) revenue growth percentages calculated via LAG() OVER to monitor baseline momentum.

---

## Python Analytics Results

### 1. RFM Customer Segmentation
Customers were scored on a 1-4 scale based on Recency (days since last purchase), Frequency (number of unique transaction dates), and Monetary (total value of purchases).
* Champions (6 customers): High-frequency, high-value accounts with recent activity.
* Loyal Customers (16 customers): Steady purchasing frequency and revenue contribution.
* Potential / Others (11 customers): Average scores; moderate buying frequency.
* At Risk (2 customers): Previously valuable accounts with high recency intervals.
* Lost Customers (17 customers): Low recency, low frequency, and low value.

### 2. Pareto (80/20) Analysis
The customer base exhibits extreme revenue concentration:
* Top 10 customers generate 80.6% of total revenue.
* 19.2% of the customer base (10 out of 52 active accounts) drives 80% of total sales volume.
* This highlights a high customer concentration risk, indicating that losing a single top-tier account would significantly impact overall cash flow.

### 3. ABC Product Classification
Products were grouped into tiers based on cumulative revenue contribution:
* A Class (29 products): Drives 69.4% of revenue. Requires tight inventory control and active replenishment monitoring.
* B Class (58 products): Drives 20.5% of revenue. Requires moderate control.
* C Class (161 products): Drives 10.1% of revenue. Low value; suggests opportunities for SKU rationalization to reduce warehousing costs.

### 4. Cohort Retention Analysis
A monthly cohort retention analysis was executed using transaction month offsets from each customer's first purchase month.
* B2B Purchase Cycles: While the analysis executed successfully, the retention matrix shows highly irregular purchasing intervals rather than traditional linear decay.
* Operational Conclusion: Retention curves and heatmaps are less representative for B2B accounts that purchase on variable replenishment cycles or project-based orders compared to subscription (SaaS) or retail settings.

---

## Key Insights and Business Recommendations

* Mitigate Concentration Risk: Since 19% of customers generate 80% of revenue, the company should establish dedicated key account management teams to lock in long-term service agreements with the top 10 accounts.
* SKU Rationalization: Class C products represent 65% of the catalog but contribute only 10% of revenue. Standardizing components or phasing out low-demand Class C parts can reduce production complexity and holding costs.
* Customer Win-Back: The two accounts flagged as "At Risk" represent high-frequency historical buyers who have not purchased recently. Sales representatives should target these accounts immediately with custom retention campaigns.
* RFM Allocation: Focus marketing and customer service resources on the 16 "Loyal Customers" to transition them into "Champions" through volume discounts or product cross-selling.

---

## Tools Used

* Python: pandas, numpy, matplotlib
* SQL: MySQL / Redshift compatible syntax for analytic aggregates
* Power BI: Star schema data modeling (implemented locally)
