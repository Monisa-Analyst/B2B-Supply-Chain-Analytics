# GitHub Publication Checklist

Use this checklist prior to pushing this repository to a public GitHub workspace. It ensures no sensitive customer or financial data is exposed.

---

## Pre-Publication Verification Steps

### 1. Data Verification
- [ ] Confirm that no `.csv` file is tracked or staged in the Git repository. Run `git status` to verify.
- [ ] Confirm that no `.pbix` file is tracked or staged in the Git repository.
- [ ] Verify that mapping logs (`customer_mapping.csv`, `product_mapping.csv`) are ignored by Git.

### 2. Output and Visual Verification
- [ ] Verify that `RFM_Segments.png`, `Pareto_Chart.png`, and `Cohort_Heatmap.png` are the only output assets in the `outputs/` directory.
- [ ] Review these output charts to confirm no real customer names, part numbers, or corporate headers are printed on the axes, legends, or titles.

### 3. SQL Script Verification
- [ ] Review all SQL scripts in the `sql/` directory. Ensure they are identical to your original local SQL scripts and contain no hardcoded real customer names.

### 4. Notebook Verification
- [ ] Open the notebook `python/Manufacturing_Sales_Analytics.ipynb` and verify that the code cells are identical to your local development notebook.

### 5. Git and Ignored Files
- [ ] Run `git status` to verify that the working tree is clean and that `.gitignore` correctly blocks all CSV and PBIX patterns.
