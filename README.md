# parse-ny-sutax-pdf
Extract state and county sales and use taxes from NYS provided PDF. This was written years ago, uploading and will refactor. 

This simply extracts and separates sales and use tax rates from NYS Publication 718 (See: https://www.tax.ny.gov/pubs_and_bulls/tg_bulletins/st/sales_tax_rate_publications.htm).

See program.py for implementation. 

01_county_match.py and 02_city_match.py is just super quick script I wrote to join the extracted data to a GEOID/ANSI/FIPS for import into a relational database. The implementation is very rudimentary and doesn't handle localities that don't have a match such as NYC boroughs. It's quick and dirty, using pandas to join NY boundary data and the extracted rates on a string key (locality name). The purpose of this was to get some seed data MSSQL as part of a bigger project.