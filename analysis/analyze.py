import pandas as pd
import numpy as np
import json

df = pd.read_excel('/mnt/user-data/uploads/disease_outbreaks_HDX.xlsx')
df.columns = [c.strip() for c in df.columns]
# Drop the HXL tag row
df = df[df['id_outbreak'] != '#Year+iso3+icd4'].copy()
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

print("Rows:", len(df))
print("Year range:", df['Year'].min(), df['Year'].max())
print("Is covid flag count:", (df['Disease'] == 'COVID-19').sum())

# Exclude COVID dashboard entries and 2026 partial year for the "true outbreak event" picture
df_core = df[(df['Disease'] != 'COVID-19')].copy()
print("Non-COVID rows:", len(df_core))

# ---- COUNTRY RECURRENCE ANALYSIS ----
# For each country: which years (1996-2025, excluding partial 2026) had at least one non-COVID outbreak event
analysis_years = range(1996, 2026)  # exclude 2026 partial
df_years = df_core[df_core['Year'].isin(analysis_years)].copy()

country_year = df_years.groupby(['Country', 'iso3'])['Year'].apply(lambda x: sorted(set(x))).reset_index()
country_year['n_years_active'] = country_year['Year'].apply(len)
total_years = len(analysis_years)
country_year['pct_years_active'] = country_year['n_years_active'] / total_years * 100
country_year['n_events'] = df_years.groupby(['Country','iso3']).size().values
country_year['n_diseases'] = df_years.groupby(['Country','iso3'])['Disease'].nunique().values

country_year = country_year.sort_values('n_years_active', ascending=False).reset_index(drop=True)
print("\n--- TOP 20 MOST CHRONIC COUNTRIES (years active out of 30) ---")
print(country_year[['Country','n_years_active','pct_years_active','n_events','n_diseases']].head(20).to_string())

print("\n--- COUNTRIES ACTIVE IN ONLY 1 OR 2 YEARS (appear once/rarely) ---")
rare = country_year[country_year['n_years_active'] <= 2].sort_values('n_years_active')
print(f"Count of countries with <=2 years active: {len(rare)}")
print(rare[['Country','n_years_active','n_events','n_diseases']].to_string())

print("\n--- COUNTRIES ACTIVE IN EXACTLY 1 YEAR ---")
once = country_year[country_year['n_years_active'] == 1]
print(f"Count: {len(once)}")
print(once[['Country','Year','n_events']].to_string())

# Total countries in dataset
print("\nTotal distinct countries (non-COVID, 1996-2025):", country_year['Country'].nunique())

# ---- GAP ANALYSIS: find longest gaps for recurring countries ----
def longest_gap(years):
    years = sorted(years)
    if len(years) < 2:
        return 0
    gaps = [years[i+1]-years[i] for i in range(len(years)-1)]
    return max(gaps)

country_year['longest_gap'] = country_year['Year'].apply(longest_gap)
country_year['first_year'] = country_year['Year'].apply(min)
country_year['last_year'] = country_year['Year'].apply(max)

# ---- MPOX / RE-EMERGENCE STORY ----
mpox_names = [d for d in df['Disease'].unique() if 'pox' in str(d).lower() or 'mpox' in str(d).lower()]
print("\nMpox-related disease names found:", mpox_names)
mpox = df[df['Disease'].isin(mpox_names)]
mpox_by_year = mpox.groupby('Year').agg(n_events=('Country','count'), n_countries=('Country','nunique')).reset_index()
print("\n--- MPOX/MONKEYPOX BY YEAR ---")
print(mpox_by_year.to_string())

# ---- OVERALL YEARLY NON-COVID EVENT COUNTS (for context chart) ----
yearly = df_core[df_core['Year'].isin(analysis_years)].groupby('Year').agg(
    n_events=('Country','count'), n_countries=('Country','nunique'), n_diseases=('Disease','nunique')
).reset_index()
print("\n--- YEARLY EVENTS (non-COVID, 1996-2025) ---")
print(yearly.to_string())

# Save key artifacts for narrative-building
country_year_out = country_year.copy()
country_year_out['Year'] = country_year_out['Year'].apply(lambda yrs: ','.join(str(y) for y in yrs))
country_year_out.to_csv('country_recurrence.csv', index=False)
yearly.to_csv('yearly_events.csv', index=False)
mpox_by_year.to_csv('mpox_by_year.csv', index=False)
df.to_csv('outbreaks_clean_full.csv', index=False)
df_core.to_csv('outbreaks_noncovid.csv', index=False)

print("\nSaved: country_recurrence.csv, yearly_events.csv, mpox_by_year.csv, outbreaks_clean_full.csv, outbreaks_noncovid.csv")
