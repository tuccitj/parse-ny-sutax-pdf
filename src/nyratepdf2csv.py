import pandas as pd
import tabula
class NYPub718Parser(object):
    def __init__(self, pub718_path) -> None:
        df = tabula.read_pdf(pub718_path, multiple_tables=True, pages='all')
        df = self._drop_unnamed_cols(df)
        keys = [df[0].keys()[0:2], df[0].keys()[2:4], df[0].keys()[4:6]]
        df000 = [self._parse_dataframe(df[0][key]) for key in keys]
        df_final = pd.concat(df000)
        df_final = self._handle_nyc_anomalies(df_final)
        df_final = self._finalize_formatting(df_final)
        self.result_aggregate = df_final
        self.result_county_rates = self._get_county_rates(df_final)
        self.result_city_rates = self._get_city_rates(df_final)
    def _drop_unnamed_cols(self, df):
        cols_to_drop = [key for key in df[0].keys() if ("Unnamed" in key)]
        df[0] = df[0].drop(columns=cols_to_drop)
        return df
    def _convert_rate(self, rate):
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
    def _handle_nyc_anomalies(self, df):
        nyc = df.loc[df['county'].str.contains('\\*New York City')]
        print(nyc)
        df.loc[df.county.str.contains(
            'New York City'), 'reporting_code'] = '8081'

        df.loc[df.county.str.contains(
            'New York City'), 'rate'] = float(nyc['rate'])

        df = df.replace(
            {'\\*': '', ' – see New York City': '', ' – except': ''}, regex=True).copy()

        return df
    def _parse_dataframe(self, df):
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
            lambda rate: self._convert_rate(rate))
        return df
    def _finalize_formatting(self, df):
        df['county'] = df['county'].str.strip().copy()
        df['reporting_code'] = df['reporting_code'].str.strip().copy()
        return df
    def _get_county_rates(self, df):
        county_rates = df[df["county"].str.contains("city") == False]
        return county_rates
    def _get_city_rates(self, df):
        city_rates = df.loc[df.county.str.contains('city')]
        city_rates = city_rates.replace({' \\(city\\)': ''}, regex=True).copy()
        city_rates.columns = ['city', 'reporting_code', 'rate']
        return city_rates
# tabula extracts tables from PDFs
# df = tabula.read_pdf('docs/core/pub718.pdf', multiple_tables=True, pages='all')
parser = NYPub718Parser('docs/core/pub718.pdf')
parser.result_aggregate.to_csv("docs/output/ny_rates_aggregate.csv", index=False)
parser.result_county_rates.to_csv("docs/output/ny_county_rates.csv", index=False)
parser.result_city_rates.to_csv("docs/output/ny_city_rates.csv", index=False)
