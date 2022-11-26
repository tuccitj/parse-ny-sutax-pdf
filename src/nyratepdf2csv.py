import pandas as pd
import tabula

def convert_rate(rate):
    result = rate
    # eg 81/8 (8 + (1/2))/100 rounded to 5 decimal places
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

def handle_nyc_anomalies(df):
    nyc = df.loc[df['county'].str.contains('\\*New York City')]

    df.loc[df.county.str.contains(
        'New York City'), 'reporting_code'] = '8081'

    df.loc[df.county.str.contains(
        'New York City'), 'rate'] = float(nyc['rate'])

    df = df.replace(
        {'\\*': '', ' – see New York City': '', ' – except': ''}, regex=True).copy()

    return df

def parse_dataframe(df):
    # rename columns
    df.columns = ['county', 'reporting_code']
    # drop first row
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

    return df

def finalize_formatting(df):
    df['county'] = df['county'].str.strip().copy()
    df['reporting_code'] = df['reporting_code'].str.strip().copy()
    return df

# tabula extracts tables from PDFs
df = tabula.read_pdf('docs/core/pub718.pdf', multiple_tables=True, pages='all')
cols_to_drop = [key for key in df[0].keys() if ("Unnamed" in key)]
df[0] = df[0].dromovrdp(columns=cols_to_drop)
keys = [df[0].keys()[0:2], df[0].keys()[2:4], df[0].keys()[4:6]]
df000 = [parse_dataframe(df[0][key]) for key in keys]
df_final = pd.concat(df000)
df_final = handle_nyc_anomalies(df_final)
df_final = finalize_formatting(df_final)


county_rates = df_final[df_final["county"].str.contains("city") == False]
county_rates.to_csv("docs/output/ny_county_rates.csv", index=False)

city_rates = df_final.loc[df_final.county.str.contains('city')]
city_rates = city_rates.replace(
    {' \\(city\\)': ''}, regex=True).copy()
city_rates.columns = ['city', 'reporting_code', 'rate']
city_rates.to_csv("docs/output/ny_city_rates.csv", index=False)
