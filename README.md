# Manufacturing Sales & Customer Intelligence Platform

An end-to-end data analytics and business intelligence project transforming raw B2B manufacturing sales register data into strategic customer and product intelligence. This project utilizes SQL, Python, and Power BI to analyze purchasing behavior, segment customer accounts, classify product inventory, and map revenue concentration risks.

---

## Project Overview

B2B manufacturing suppliers often struggle to extract actionable insights from traditional ERP ledgers. In this project, raw sales transaction ledger data exported from Tally ERP was cleaned, structured, and analyzed to support executive decisions.

The platform provides visibility into:
1. **Customer Segments**: Scoring customers on Recency, Frequency, and Monetary (RFM) metrics to group them into actionable business tiers (Champions, Loyal, At Risk, Lost).
2. **Revenue Concentration**: Applying Pareto (80/20) analysis to measure key customer dependencies.
3. **Product Classification**: Categorizing inventory using ABC classification based on revenue contribution.
4. **Retention Metrics**: Analyzing cohort retention rates to evaluate customer lifecycle patterns.

---

## Repository Structure

```
Manufacturing-Sales-Customer-Intelligence-Platform/
├── data/
│   └── FactSales_Anonymized.csv         # Cleaned, anonymized sales transaction ledger
├── sql/
│   ├── 01_Revenue_Analysis.sql          # Monthly sales aggregates and threshold queries
│   ├── 02_Customer_Analysis.sql         # Customer revenue rankings and share percentages
│   ├── 03_Product_Analysis.sql          # Product sales volume and quantity rankings
│   └── 04_Growth_Analysis.sql           # Period-over-period growth and cumulative trends
├── python/
│   ├── RFM_Analysis.py                  # RFM scoring and customer segmentation engine
│   ├── Pareto_Analysis.py               # Customer concentration analysis and Pareto charting
│   ├── ABC_Classification.py            # Product portfolio revenue tiering (A/B/C)
│   └── Cohort_Analysis.py               # Cohort customer retention matrix generator
├── dashboard/
│   ├── Manufacturing_Sales_Analytics.pbix # Power BI dashboard report template
│   └── screenshots/                     # Page views of the interactive dashboards
├── outputs/
│   ├── RFM_Results.csv                  # Calculated customer scores and segment labels
│   ├── RFM_Segments.png                 # Segment customer count & revenue contribution plot
│   ├── Pareto_Results.csv               # Cumulative revenue table by customer
│   ├── Pareto_Chart.png                 # Dual-axis Pareto chart
│   ├── ABC_Results.csv                  # ABC classification table by product SKU
│   ├── ABC_Classification.png           # SKU count share vs revenue contribution plot
│   ├── Cohort_Output.csv                # Cohort retention percentage matrix
│   └── Cohort_Heatmap.png               # Customer retention rate monthly heatmap
└── docs/
    ├── Data_Privacy_Audit.md            # Privacy policies and anonymization details
    └── GitHub_Publication_Checklist.md   # Step-by-step verification checklist
```

---

## Dataset Description

The dataset covers 2.5 years of transactional data (April 2024 to June 2026) containing 1,839 sales line items. The schema is modeled as follows:

* **Date**: Transaction timestamp (DD-MMM-YY format).
* **Customer**: Anonymized buyer label (Customer A, Customer B, etc.).
* **Products**: Anonymized SKU identifier (Product 001, Product 002, etc.).
* **Quantity**: Number of units sold.
* **Rate**: Price per unit (scaled to protect financial confidentiality).
* **Revenue**: Total transaction value (Quantity * Rate).

---

## Data Engineering and Modeling

1. **Extraction and Cleaning**: The raw ERP export was cleaned in Excel and Power Query. Extraneous header blocks, empty rows, and total lines were filtered. Corporate buyer names and physical parts were mapped to standardized, anonymized labels.
2. **Data Scaling**: Rate and revenue figures were scaled by a factor of 1.37. This prevents the reconstruction of the company's real financial statements while preserving all mathematical rankings, proportions, and analytics outputs.
3. **Star Schema Model**: Loaded into Power BI using a star schema design:
   * `FactSales`: Transaction details (Date, Customer, Products, Quantity, Rate, Revenue).
   * `DimCustomer` (via `customer_mapping`): Customer metadata (aliases).
   * `DimProduct` (via `product_mapping`): Product catalog attributes.
   * `DimCalendar` (via `DimCalendar` DAX query): Automated calendar dimension supporting time-intelligence queries.

---

## SQL Analysis

The `sql/` directory contains standard queries used to extract key operational reports from the data:
* **Revenue Performance**: Monthly revenue aggregates, running totals, and target threshold filters (identifying periods falling below targets).
* **Customer Performance**: Absolute sales rankings and cumulative revenue shares using window functions (`RANK() OVER` and `SUM() OVER`).
* **Product Velocity**: SKU sales rankings by total units sold and net revenue generated.
* **Growth Metrics**: Month-over-month (MoM) revenue growth percentages calculated via `LAG() OVER` to monitor baseline momentum.

---

## Python Analytics Results

### 1. RFM Customer Segmentation
Customers were scored on a 1-4 scale based on Recency (days since last purchase), Frequency (number of unique transaction dates), and Monetary (total value of purchases).
* **Champions** (6 customers): High-frequency, high-value accounts with recent activity.
* **Loyal Customers** (16 customers): Steady purchasing frequency and revenue contribution.
* **Potential / Others** (11 customers): Average scores; moderate buying frequency.
* **At Risk** (2 customers): Previously valuable accounts with high recency intervals.
* **Lost Customers** (17 customers): Low recency, low frequency, and low value.

### 2. Pareto (80/20) Analysis
The customer base exhibits extreme revenue concentration:
* **Top 10 customers** generate **80.6%** of total revenue.
* **19.2%** of the customer base (10 out of 52 active accounts) drives **80%** of total sales volume.
* This highlights a high customer concentration risk, indicating that losing a single top-tier account would significantly impact overall cash flow.

### 3. ABC Product Classification
Products were grouped into tiers based on cumulative revenue contribution:
* **A Class** (29 products): Drives **69.4%** of revenue (approximately ₹7.77 Cr scaled). Requires tight inventory control and active replenishment monitoring.
* **B Class** (58 products): Drives **20.5%** of revenue (approximately ₹2.30 Cr scaled). Requires moderate control.
* **C Class** (161 products): Drives **10.1%** of revenue (approximately ₹1.12 Cr scaled). Low value; suggests opportunities for SKU rationalization to reduce warehousing costs.

### 4. Cohort Retention Analysis
A monthly cohort retention analysis was executed using transaction month offsets from each customer's first purchase month.
* **B2B Purchase Cycles**: While the analysis executed successfully, the retention matrix shows highly irregular purchasing intervals rather than traditional linear decay.
* **Operational Conclusion**: Retention curves and heatmaps are less representative for B2B accounts that purchase on variable replenishment cycles or project-based orders compared to subscription (SaaS) or retail settings.

---

## Power BI Dashboard Pages

The interactive dashboard (`dashboard/Manufacturing_Sales_Analytics.pbix`) is designed across five sections:

1. **Executive Overview**: Central scorecard showing core KPIs (Total Revenue, Total Customers, Active SKUs, Quantity Sold) and trend lines for monthly revenue and regional distributions.
2. **Customer Intelligence**: Detailed RFM segment dashboard showing segment distribution, customer count counts, and individual KPI drill-downs.
3. **Product Intelligence**: Treemap visualizations of SKU contributions grouped by ABC class, allowing inventory managers to identify low-velocity SKUs.
4. **Pareto Analysis**: Dual-axis bar and line visualization of customer contribution, highlighting the 80% cutoff boundary.
5. **Strategic Business Recommendations**: Summary slide containing key analytical conclusions and data-driven recommendations for sales teams.

---

## Key Insights and Business Recommendations

* **Mitigate Concentration Risk**: Since 19% of customers generate 80% of revenue, the company should establish dedicated key account management teams to lock in long-term service agreements with the top 10 accounts.
* **SKU Rationalization**: Class C products represent 65% of the catalog but contribute only 10% of revenue. Standardizing components or phasing out low-demand Class C parts can reduce production complexity and holding costs.
* **Customer Win-Back**: The two accounts flagged as "At Risk" represent high-frequency historical buyers who have not purchased recently. Sales representatives should target these accounts immediately with custom retention campaigns.
* **RFM Allocation**: Focus marketing and customer service resources on the 16 "Loyal Customers" to transition them into "Champions" through volume discounts or product cross-selling.

---

## Tools Used

* **Python**: pandas, numpy, matplotlib
* **SQL**: MySQL / Redshift compatible syntax for analytic aggregates
* **Power BI**: Star schema data modeling, interactive dashboard design, DAX measures
