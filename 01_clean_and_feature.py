import pandas as pd
import numpy as np

df = pd.read_csv('data/retail_price.csv')

# --- Parse date ---
df['date'] = pd.to_datetime(df['month_year'], format='%d-%m-%Y')

# --- Sanity check: total_price should equal qty * unit_price ---
df['check_total'] = (df['qty'] * df['unit_price']).round(2)
mismatch = (df['check_total'] - df['total_price']).abs() > 0.5
print(f"Rows where qty*unit_price != total_price: {mismatch.sum()} / {len(df)}")

# --- Competitor pricing context ---
df['avg_competitor_price'] = df[['comp_1', 'comp_2', 'comp_3']].mean(axis=1)
df['price_gap_pct'] = (df['unit_price'] - df['avg_competitor_price']) / df['avg_competitor_price'] * 100

# --- Revenue & margin proxy (no cost data available, so we track revenue only) ---
df['revenue'] = df['qty'] * df['unit_price']

# --- Log transforms for elasticity regression ---
df['log_qty'] = np.log(df['qty'])
df['log_price'] = np.log(df['unit_price'])

# --- Tidy final table ---
cols = [
    'product_id', 'product_category_name', 'date', 'year', 'month',
    'qty', 'unit_price', 'avg_competitor_price', 'price_gap_pct',
    'revenue', 'log_qty', 'log_price',
    'product_score', 'customers', 'weekend', 'holiday'
]
clean = df[cols].sort_values(['product_category_name', 'product_id', 'date']).reset_index(drop=True)
clean.to_csv('outputs/clean_pricing_data.csv', index=False)

print(clean.shape)
print(clean.head(10))
print()
print("Rows per category:")
print(clean.groupby('product_category_name').size())
