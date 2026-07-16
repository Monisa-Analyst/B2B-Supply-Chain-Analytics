# GitHub Publication Checklist

Use this checklist prior to pushing this repository to a public GitHub workspace. It ensures no sensitive customer or financial data is exposed.

---

## Pre-Publication Verification Steps

### 1. Data Verification
- [ ] Confirm that `data/FactSales.csv` is the only dataset in the `data/` folder.
- [ ] Verify that no real customer names (e.g., Aldica, Suprajit, Teknic) exist in `FactSales.csv`.
- [ ] Verify that no real product names or physical part numbers exist in `FactSales.csv`.
- [ ] Confirm that the total row count in `FactSales.csv` is exactly 1,839.

### 2. Output and Visual Verification
- [ ] Verify that all outputs in the `outputs/` folder (`RFM_Output.csv`, `Pareto_Output.csv`, `ABC_Output.csv`, `Cohort_Output.csv`) contain only anonymized names (Customer A, Product 001).
- [ ] Review `RFM_Segments.png`, `Pareto_Chart.png`, and `Cohort_Heatmap.png` to confirm no real company names or leaked identifiers are printed in the titles, legends, or axes labels.

### 3. SQL Script Verification
- [ ] Review all SQL scripts in the `sql/` directory. Ensure they match your original code structure (referencing `Value ( Quantity * Rate )` and `factsales` table).
- [ ] Confirm there are no hardcoded customer or product names in the SQL comments or WHERE clauses.

### 4. Power BI File Cache Clearance
- [ ] Open the Power BI dashboard (`dashboard/Manufacturing_Sales_Analytics_.pbix`) in Power BI Desktop.
- [ ] Navigate to Transform Data -> Data Source Settings and change the file paths for the tables (`FactSales`, `RFM_Output`, `ABC_Output`, `Pareto_Output`) to point to the newly generated anonymized CSV files in the `data/` and `outputs/` directories.
- [ ] Click Close & Apply and wait for the queries to refresh completely.
- [ ] Confirm that the visuals (customer ranks, segments) match the anonymized names.
- [ ] Save the `.pbix` file. This clears the old data cache and stores the anonymized dataset inside the Power BI file structure.

### 5. Git and Ignored Files
- [ ] Run `git status` to verify that no mapping files (`customer_mapping.csv`, `product_mapping.csv`) or raw datasets are staged for commit.
- [ ] Confirm that `.gitignore` is correctly located at the root of the workspace.
