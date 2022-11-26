import pandas as pd

df0 = pd.read_csv('docs/output/ny_county_rates.csv')
# create key field based on county name
df0['key'] = df0['county'].str.upper()
print(df0)
df1 = pd.read_csv('docs/core/ny_counties.csv')
# create key column from NAMELSAD which will match with county name
df1['key'] = df1['NAMELSAD'].str.upper()
# remove the word COUNTY so it will map properly
df1['key'] = df1['key'].str.replace(' COUNTY', '')
print(df1)
# merge on the new key
merged = df0.merge(df1, left_on='key', right_on='key')
# select only the columns we need
merged = merged[['COUNTYNS', 'county', 'reporting_code', 'rate']]
# rename columnss
merged.columns = [['jurisdiction_place_id',
                   'county', 'reporting_code', 'rate']]
# output to csv
merged.to_csv('docs/output/ny_city_rates_merged.csv', index=False)
