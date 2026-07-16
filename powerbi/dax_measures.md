# Power BI DAX Measures

This document details the DAX (Data Analysis Expressions) formulas created in the Power BI model to calculate executive KPI scorecards and support visual metrics.

---

## Executive Overview KPI Measures

### 1. Total Revenue
Calculates the aggregate gross revenue across all transactions.
```dax
Total Revenue = SUM(FactSales[Value ( Quantity * Rate )])
```

### 2. Total Customers
Calculates the count of unique corporate customer accounts active in the system.
```dax
Total Customers = DISTINCTCOUNT(FactSales[Customer])
```

### 3. Total Products
Calculates the count of unique product SKUs sold.
```dax
Total Products = DISTINCTCOUNT(FactSales[Products])
```

### 4. Total Quantity
Sums the net physical units sold across all order line items.
```dax
Total Quantity = SUM(FactSales[Quantity])
```

### 5. Average Revenue per Customer
Computes the mean sales value generated per customer account.
```dax
Average Revenue per Customer = DIVIDE([Total Revenue], [Total Customers], 0)
```
