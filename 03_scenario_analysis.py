import pandas as pd
import numpy as np

res = pd.read_csv('outputs/elasticity_by_category.csv')

# Scenario: what if price is realigned to match average competitor price
# (i.e. close the price_gap_pct to 0)? Only apply to categories where
# elasticity is statistically significant, since we don't trust the others.
sig = res[res['classification'].isin(['Elastic (protect volume)', 'Inelastic (price opportunity)'])].copy()

sig['price_change_pct'] = -sig['avg_price_gap_vs_competitors_pct']  # move toward competitor price
sig['qty_change_pct'] = sig['elasticity'] * sig['price_change_pct']
sig['new_price'] = sig['avg_price'] * (1 + sig['price_change_pct']/100)
sig['new_qty'] = sig['avg_qty_per_month'] * (1 + sig['qty_change_pct']/100)
sig['revenue_change_pct'] = ((1 + sig['price_change_pct']/100) * (1 + sig['qty_change_pct']/100) - 1) * 100
sig['current_annual_revenue'] = sig['total_revenue']  # already summed across ~13-20 months in data; treat as historical total
sig['projected_revenue_change'] = sig['current_annual_revenue'] * sig['revenue_change_pct'] / 100

out = sig[['category','elasticity','avg_price_gap_vs_competitors_pct','price_change_pct',
           'revenue_change_pct','current_annual_revenue','projected_revenue_change']].sort_values(
           'projected_revenue_change', ascending=False)

out.to_csv('outputs/pricing_scenario_impact.csv', index=False)
print(out.to_string(index=False))
print()
print(f"Total projected revenue upside from realigning elastic, overpriced categories: {out[out.projected_revenue_change>0].projected_revenue_change.sum():,.0f}")
