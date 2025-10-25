import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

arc_data = pd.read_csv("county_economic_status_2024.csv", skiprows=4, skipfooter=1, engine='python', thousands=',')

arc_data.columns = ['fips', 'state', 'county', 'arc_county',
    'economic_status', 'unemp_rate_3yr',
    'income_pc', 'poverty_rate',
    'unemp_pct_us', 'income_pct_us',
    'income_pct_us_inv', 'poverty_pct_us',
    'composite_index', 'index_rank', 'quartile']

print(arc_data.head())

mean_poverty = arc_data['poverty_rate'].mean()
std_poverty = arc_data['poverty_rate'].std()
min_poverty = arc_data['poverty_rate'].min()
max_poverty = arc_data['poverty_rate'].max()

print("=== Poverty Rate Statistics (All Counties) ===")
print(f"Mean Poverty Rate: {mean_poverty:.2f}%")
print(f"Standard Deviation: {std_poverty:.2f}")
print(f"Minimum Poverty Rate: {min_poverty:.2f}%")
print(f"Maximum Poverty Rate: {max_poverty:.2f}%")
print("=============================================")