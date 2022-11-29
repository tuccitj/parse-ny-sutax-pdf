from nyratepdf2csv import NYPub718Parser
# tabula extracts tables from PDFs
# df = tabula.read_pdf('docs/core/pub718.pdf', multiple_tables=True, pages='all')
parser = NYPub718Parser('docs/core/pub718.pdf')

parser.result_aggregate.to_csv("docs/output/ny_rates_aggregate.csv", index=False)
parser.result_county_rates.to_csv("docs/output/ny_county_rates.csv", index=False)
parser.result_city_rates.to_csv("docs/output/ny_city_rates.csv", index=False)