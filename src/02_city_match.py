import pandas as pd

df0 = pd.read_csv('docs/output/ny_city_rates.csv')
df0['key'] = df0['city'].str.upper()
df1 = pd.read_csv('docs/core/ny_cities.csv')
df1 = df1.loc[df1['NAMELSAD'].str.contains('city')]
df1['key'] = df1['NAMELSAD'].str.upper()
df1['key'] = df1['key'].str.replace(' CITY', '')
merged = df0.merge(df1, left_on='key', right_on='key')
merged = merged[['PLACENS', 'city', 'reporting_code', 'rate']]
merged.columns = [['jurisdiction_place_id',
                   'city', 'reporting_code', 'rate']]
print(merged)
merged.to_csv('docs/output/ny_city_rates_merged.csv', index=False)
