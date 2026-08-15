# Pricing & Revenue Optimization Diagnostic

A consulting-style data diagnostic: given a retail product portfolio (9 categories,
52 SKUs, 15 months of monthly price/quantity/competitor data), identify where the
business can adjust pricing to improve revenue without hurting demand.

## Method
1. **Data cleaning & feature engineering** (`scripts/01_clean_and_feature.py`) —
   parsed dates, computed competitor price gap, log-transformed price/quantity.
2. **Price elasticity estimation** (`scripts/02_elasticity_analysis.py`) — for each
   category, ran a log-log OLS regression of quantity on price with product-level
   fixed effects, to isolate the true price effect from product popularity.
3. **Scenario modeling** (`scripts/03_scenario_analysis.py`) — quantified the
   revenue impact of realigning price to the competitor benchmark, for categories
   with statistically significant elasticity.

## Key finding
No category showed a confident opportunity to *raise* prices — every
statistically significant category was highly price-elastic. The real
opportunity was **Watches & Gifts**, priced 12.8% above competitors despite being
elastic: realigning its price down is projected to lift category revenue ~21%.

## Files
- `clean_pricing_data.csv` — cleaned transaction-level dataset
- `elasticity_by_category.csv` — elasticity estimates and significance by category
- `pricing_scenario_impact.csv` — projected revenue impact of price realignment
- `Pricing_Optimization_Memo.docx` — one-page executive recommendation memo
- `PowerBI_Build_Guide.md` — instructions to build the accompanying dashboard
- `scripts/` — full analysis pipeline in Python (pandas, statsmodels)

## Data source
Adapted from a public retail pricing dataset (Olist e-commerce, Brazil),
originally sourced via Kaggle.

## Tools
Python (pandas, statsmodels) for analysis · Power BI for visualization
