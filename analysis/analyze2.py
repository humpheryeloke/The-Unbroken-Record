import pandas as pd
import numpy as np

df = pd.read_csv('outbreaks_noncovid.csv')
cr = pd.read_csv('country_recurrence.csv')

analysis_years = range(1996, 2026)
df_years = df[df['Year'].isin(analysis_years)].copy()

# Top 12 chronic countries - disease breakdown
top12 = cr.sort_values('n_years_active', ascending=False).head(12)['Country'].tolist()
print("TOP 12:", top12)
for c in top12:
    sub = df_years[df_years['Country']==c]
    top_dis = sub['Disease'].value_counts().head(5)
    print(f"\n{c} ({sub['Year'].nunique()} years, {len(sub)} events):")
    print(top_dis.to_string())

# DRC detail - gap analysis
drc = df_years[df_years['Country']=="Congo Democratic Republic of the"]
drc_years = sorted(drc['Year'].unique())
print("\nDRC years present:", drc_years)
print("DRC years MISSING (out of 1996-2025):", sorted(set(analysis_years) - set(drc_years)))

# One-off countries detail with disease + region
once = cr[cr['n_years_active']==1].copy()
once_detail = df_years.merge(once[['Country']], on='Country')[['Country','Year','Disease','who_region','unsd_subregion']]
print("\n--- ONE-OFF COUNTRIES DETAIL ---")
print(once_detail.sort_values('Year').to_string())

# Region share of chronic (>=15 yrs) vs one-off countries
chronic15 = cr[cr['n_years_active']>=15]
print(f"\nCountries with >=15/30 years active: {len(chronic15)}")
print(f"Countries with <=2/30 years active: {len(cr[cr['n_years_active']<=2])}")
print(f"Median years active across all {len(cr)} countries:", cr['n_years_active'].median())
print(f"Mean years active:", cr['n_years_active'].mean())

# distribution buckets
bins = [0,1,2,5,10,15,20,25,31]
cr['bucket'] = pd.cut(cr['n_years_active'], bins=bins)
print("\nDistribution of years-active buckets:")
print(cr['bucket'].value_counts().sort_index().to_string())

# mpox gap detail
mpox = pd.read_csv('mpox_by_year.csv')
print("\nmpox full timeline:\n", mpox.to_string())
# gap between 1997 and 2016
print("Gap 1997->2016 = 19 years with zero mpox DONs")

# who region breakdown of chronic vs rare
who_chronic = df_years[df_years['Country'].isin(chronic15['Country'])]['who_region'].value_counts()
who_rare = df_years[df_years['Country'].isin(once['Country'])]['who_region'].value_counts()
print("\nWHO region of chronic-country events:\n", who_chronic.to_string())
print("\nWHO region of one-off-country events:\n", who_rare.to_string())
