# Setup and validation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
pd.set_option('display.max_columns', None)

# Read the sales ledger
df = pd.read_csv("FactSales.csv")
df = df.rename(columns={
    'Value ( Quantity * Rate )': 'Revenue'
})
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

# RFM Analysis
snapshot_date = df['Date'].max() + pd.Timedelta(days=1)
print("Snapshot date used for Recency calculation:", snapshot_date.date())

rfm = df.groupby('Customer').agg(
    Recency=('Date', lambda x: (snapshot_date - x.max()).days),
    Frequency=('Date', 'nunique'),
    Monetary=('Revenue', 'sum')
).reset_index()

# Scoring
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4]).astype(int)

rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

def assign_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['F_Score'] >= 3 and row['M_Score'] >= 3:
        return 'Loyal Customers'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return 'At Risk'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return 'Lost Customers'
    else:
        return 'Potential / Others'

rfm['Segment'] = rfm.apply(assign_segment, axis=1)

# Summary table
segment_summary = rfm.groupby('Segment').agg(
    Customers=('Customer', 'count'),
    Total_Revenue=('Monetary', 'sum')
)
print("\nSegment Summary:\n", segment_summary)

# Plot segments
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
segment_summary['Customers'].plot(kind='bar', ax=axes[0])
segment_summary['Total_Revenue'].plot(kind='bar', ax=axes[1])
plt.tight_layout()
plt.savefig("RFM_Segments.png", bbox_inches="tight")
print("Saved RFM_Segments.png")

# Save outputs
rfm.to_csv("RFM_Output.csv", index=False)
print("Saved RFM_Output.csv")
