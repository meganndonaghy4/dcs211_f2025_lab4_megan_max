import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import requests

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

# top ten counties by decreasing poverty rate 
top_counties = arc_data.sort_values(by='poverty_rate', ascending=False).head(10)
table_pov = PrettyTable()
table_pov.field_names = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]

for _, row in top_counties.iterrows(): 
    table_pov.add_row([
        row['state'], 
        row['county'], 
        f"${row['income_pc']:,.2f}",
        f"{row['poverty_rate']:.2f}",
        f"{row['unemp_rate_3yr']:.2f}"
    ])

print(table_pov)


# function to print tables based on poverty rate, per capita income, or average unemployment 
def printTableBy(dataframe: pd.DataFrame, field: str, how_many: int, title: str
): 
    ''' 
    Function that prints a PrettyTable with the highest and lowest given amount of rows sorted by a given field. 
    Parameters: 
    - dataframe: pandas data frame 
    - field: column name (field of interest)
    - how_many: number of rows the user wants to include in the table
    - title: user's title of choice for the table
    Returns: 
    - None
    '''
    cleaned_data = dataframe.dropna(subset=[field])
    top_rows = cleaned_data.sort_values(by=field, ascending=False).head(how_many)
    bottom_rows = cleaned_data.sort_values(by=field, ascending=True).head(how_many)

    tab = PrettyTable()
    columns = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]
    tab.field_names = columns

    for _, row in top_rows.iterrows():
        tab.add_row([
        f"{row['state']:<20}",
        f"{row['county']:<20}", 
        f"${row['income_pc']:,.2f}",
        f"{row['poverty_rate']:.2f}",
        f"{row['unemp_rate_3yr']:.2f}"
    ])  

    tab.add_row(['-'*20, "-"*20, "-"*10, "-"*10, "-"*10], divider= True)

    for _, row in bottom_rows.iterrows():
        tab.add_row([
        f"{row['state']:<20}",
        f"{row['county']:<20}",
        f"${row['income_pc']:,.2f}",
        f"{row['poverty_rate']:.2f}",
        f"{row['unemp_rate_3yr']:.2f}"
    ])  
    
    print(title)
    print(tab)


#printTableBy(arc_data, 'poverty_rate', how_many = 10, title = "COUNTIES BY POVERTY RATE")
#printTableBy(arc_data, 'unemp_rate_3yr', how_many = 10, title = "COUNTIES BY UNEMPLOYMENT RATE")
#printTableBy(arc_data, 'income_pc', how_many = 10, title = "COUNTIES BY PER CAPITA INCOME")

def createByStateBarPlot(df: pd.DataFrame, field: str, filename: str, title: str, ylabel: str) -> None:
    '''
    Creates a per state bar plot for the given field, grouped by state and showing the mean value
    '''
    grouped = df.groupby('state')[field].mean().sort_values(ascending=True)

    us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
    abbrevs = [us_state_to_abbrev.get(s, s) for s in grouped.index]
    grouped.index = abbrevs

    plt.figure(figsize=(12, 6))
    plt.bar(grouped.index, grouped.values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)

    print(f"Saved plot to '{filename}'")

createByStateBarPlot(arc_data,'unemp_rate_3yr','unemploy.png','States by Poverty Rate','Average Poverty Rate (%)')
