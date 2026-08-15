import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm

df = pd.read_csv('outputs/clean_pricing_data.csv')

results = []

for cat, g in df.groupby('product_category_name'):
    n_products = g['product_id'].nunique()
    n_obs = len(g)

    try:
        if n_products > 1:
            # log-log regression with product fixed effects to control for
            # unobserved product quality/desirability
            model = smf.ols('log_qty ~ log_price + C(product_id)', data=g).fit()
        else:
            model = smf.ols('log_qty ~ log_price', data=g).fit()

        elasticity = model.params.get('log_price', np.nan)
        pval = model.pvalues.get('log_price', np.nan)
        r2 = model.rsquared

    except Exception as e:
        elasticity, pval, r2 = np.nan, np.nan, np.nan

    avg_price = g['unit_price'].mean()
    avg_qty = g['qty'].mean()
    avg_gap = g['price_gap_pct'].mean()
    total_revenue = g['revenue'].sum()

    results.append({
        'category': cat,
        'n_products': n_products,
        'n_obs': n_obs,
        'elasticity': round(elasticity, 3) if pd.notnull(elasticity) else np.nan,
        'p_value': round(pval, 4) if pd.notnull(pval) else np.nan,
        'r_squared': round(r2, 3) if pd.notnull(r2) else np.nan,
        'avg_price': round(avg_price, 2),
        'avg_qty_per_month': round(avg_qty, 1),
        'avg_price_gap_vs_competitors_pct': round(avg_gap, 1),
        'total_revenue': round(total_revenue, 0),
    })

res = pd.DataFrame(results).sort_values('elasticity')

# Classification for the recommendation
def classify(row):
    if pd.isnull(row['elasticity']):
        return 'Insufficient data'
    e = row['elasticity']
    sig = row['p_value'] < 0.10 if pd.notnull(row['p_value']) else False
    if e > -1 and sig:
        return 'Inelastic (price opportunity)'
    elif e <= -1 and sig:
        return 'Elastic (protect volume)'
    else:
        return 'Not statistically significant'

res['classification'] = res.apply(classify, axis=1)

res.to_csv('outputs/elasticity_by_category.csv', index=False)
print(res.to_string(index=False))
