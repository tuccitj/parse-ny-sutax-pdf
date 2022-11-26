import pandas as pd
import tabula

def convert_rate(rate):
    result = rate
    #eg 81/8 (8 + (1/2))/100 rounded to 5 decimal places
    if "/" in rate:
        leading_integer = int(rate[rate.index('/')-2])
        numerator = int(rate[rate.index('/')-1])
        denominator = int(rate[rate.index('/')+1])
        result = round((leading_integer + (numerator/denominator))/100, 5) 
    # for rates already that are already integers
    elif rate.isnumeric():
        result = round(int(result)/100, 5)    
    else:
        result = 0.0
        
    return result

def parse_dataframe(df):
    #rename columns
    df.columns = ['county', 'reporting_code']
    #drop first row
    df = df.drop(index=0, axis=1)
    # df['rate'] = df['county'].str.slice(start=indx)
    
    # add rate column split at first reverse space of first column
    df['rate'] = df['county'].str.rsplit(
        ' ', n=1).str[-1]
  
    df['county'] = df['county'].str.split(
        '[0-9]', n=1).str[0]
    
    # print('dfcounty',df['county'])
    # replace different encoded forward slash with regular forward slash
    df = df.replace({'⁄': '/'}, regex=True).copy()

    # apply rates
    df['rate'] = df['rate'].apply(
        lambda rate: convert_rate(rate))
    # converts fractions to decimal - refactor
    # df['rate'] = df['rate'].apply(
    #     lambda x: round((int(x[x.index('/')-2]) +
    #                     (int(x[x.index('/')-1]) /
    #                     int(x[x.index('/')+1])))/100, 5) if '/' in x else round(int(x)/100, 5) if x.isnumeric() == True else 0.0)

    return df

# tabula extracts tables from PDFs
df = tabula.read_pdf('docs/core/pub718.pdf', multiple_tables=True, pages='all'
                     )



df0 = df[0][['County or Tax', 'Reporting']].copy()
df1 = df[0][['County or Tax.1', 'Reporting.1']].copy()
df2 = df[0][['County or Tax.2', 'Reporting.2']].copy()


df0 = parse_dataframe(df0).copy()
df1 = parse_dataframe(df1).copy()
df2 = parse_dataframe(df2).copy()

df_final = pd.concat([df0, df1, df2])

nyc = df_final.loc[df_final['county'].str.contains('\\*New York City')]
# print(nyc['rate'])
# print(nyc['reporting_code'])

df_final.loc[df_final.county.str.contains(
    'New York City'), 'reporting_code'] = '8081'

df_final.loc[df_final.county.str.contains(
    'New York City'), 'rate'] = float(nyc['rate'])

df_final = df_final.replace(
    {'\\*': '', ' – see New York City': '', ' – except': ''}, regex=True).copy()
df_final['county'] = df_final['county'].str.strip().copy()
df_final['reporting_code'] = df_final['reporting_code'].str.strip().copy()

county_rates = df_final[df_final["county"].str.contains("city") == False]
county_rates.to_csv("docs/output/ny_county_rates.csv", index=False)

city_rates = df_final.loc[df_final.county.str.contains('city')]
city_rates = city_rates.replace(
    {' \\(city\\)': ''}, regex=True).copy()
city_rates.columns = ['city', 'reporting_code', 'rate']
city_rates.to_csv("docs/output/ny_city_rates.csv", index=False)


# print(df0)
# df01 = df0['County or Tax']
# rate_index = df0['County or Tax'].str.rindex(' ')
# print(rate_index)
# df0['rate'] = df0['County or Tax'].str.splice[start = 0])


# df0.columns = ['county', 'reporting_code']
# indx = (df0['county'].str.rindex(' '))

# # df0['rate'] = df0['county'].str.slice(start=indx)

# df0['rate'] = df0['county'].str.rsplit(
#     ' ', n=1).str[-1]

# df0['county'] = df0['county'].str.split(
#     '[0-9]', n=1).str[0]

# df0 = df0.replace({'⁄': '/'}, regex=True).copy()

# df0['rate'] = df0['rate'].apply(
#     lambda x: round((int(x[x.index('/')-2]) +
#                      (int(x[x.index('/')-1]) /
#                       int(x[x.index('/')+1])))/100, 5) if '/' in x else round(int(x)/100, 5) if x.isnumeric() == True else 0.0)

# print(df2)


# df0['county'].str.strip()
# df0['reporting_code'].str.strip()
# print(df0)


# indx = (df0['county'].str.rindex(' '))

# for row in df0. in
# for i in indx:
#     # print('hi: ', i)
#     print(df0['county'].str.slice(start=i))

# s1 = df0['county'].str.slice(start=)
# print(s1)

# s1 = df0['county'].str.slice(start=df0['county'].str.rindex(' '))
# for i in start_index:
#     print(df0['county'][start_index:])

# .str.slice(start_index=start_index))

# df3 = df[1]
# df3.columns = ['county', 'rate', 'reporting_code', 'county.1', 'rate.1',
#                'reporting_code.1', 'county.2', 'rate.2', 'reporting_code.2']
# print(df3)
# # print(df[0].columns)


# df0 = df[0][[]]
# print(df[1])
# df.to_csv("ny_rates_00.csv", index=False)
# tabula.convert_into("pub718.pdf", "output.csv", output_format="csv")
