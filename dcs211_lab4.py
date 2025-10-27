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

# type of state variable 
type(arc_data['state'])

# printing number of counties per state 
print(arc_data['state'].value_counts())

# table with highest ten sum stats 
state_stats = ( 
    arc_data.groupby('state')
    .agg(
        num_counties=('state', 'count'),
        mean_income_pc=('income_pc', 'mean'), 
        median_income_pc=('income_pc', 'median'),
        poverty_rate=('poverty_rate', 'mean')
    )
    .sort_values(by='num_counties', ascending=False)
    .head(10)
)

table = PrettyTable()
table.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]
for state, row in state_stats.iterrows(): 
    table.add_row([
        state,
        row['num_counties'],
        f"{row['mean_income_pc']:.2f}",
        f"{row['median_income_pc']:.2f}", 
        f"{row['poverty_rate']:.2f}"
    ])

print(table) 

# table with lowest ten sum stats (excluding DC)
state_stats_low = ( 
    arc_data
    .query("state != 'District of Columbia'")
    .groupby('state')
    .agg(
        num_counties=('state', 'count'),
        mean_income_pc=('income_pc', 'mean'), 
        median_income_pc=('income_pc', 'median'),
        poverty_rate=('poverty_rate', 'mean')
    )
    .sort_values(by='num_counties', ascending=False)
    .tail(10)
)

table_low = PrettyTable()
table_low.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]
for state, row in state_stats_low.iterrows(): 
    table_low.add_row([
        state,
        row['num_counties'],
        f"{row['mean_income_pc']:.2f}",
        f"{row['median_income_pc']:.2f}", 
        f"{row['poverty_rate']:.2f}"
    ])

print(table_low)

