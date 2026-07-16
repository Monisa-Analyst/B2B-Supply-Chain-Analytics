import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the sales ledger
df = pd.read_csv("FactSales.csv")
df = df.rename(columns={
    'Value ( Quantity * Rate )': 'Revenue'
})
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

# Cohort Analysis
df['Transaction_Month'] = df['Date'].dt.to_period('M')
df['Cohort_Month'] = df.groupby('Customer')['Date'].transform('min').dt.to_period('M')

def month_diff(row):
    return (
        (row['Transaction_Month'].year - row['Cohort_Month'].year) * 12
        + (row['Transaction_Month'].month - row['Cohort_Month'].month)
    )

df['Cohort_Index'] = df.apply(month_diff, axis=1)

cohort_data = df.groupby(['Cohort_Month', 'Cohort_Index'])['Customer'].nunique().reset_index()

cohort_counts = cohort_data.pivot(
    index='Cohort_Month',
    columns='Cohort_Index',
    values='Customer'
)

cohort_size = cohort_counts.iloc[:, 0]
retention_matrix = cohort_counts.divide(cohort_size, axis=0) * 100

print("\nRetention Matrix (first 5 rows):\n", retention_matrix.round(1).head())

# Save heatmap
fig, ax = plt.subplots(figsize=(12, 8))
data = retention_matrix.values
im = ax.imshow(data, cmap='YlGnBu', aspect='auto', vmin=0, vmax=100)
plt.colorbar(im)
plt.savefig("Cohort_Heatmap.png", bbox_inches="tight")
print("Saved Cohort_Heatmap.png")

# Save outputs
retention_matrix.to_csv("Cohort_Output.csv")
print("Saved Cohort_Output.csv")
