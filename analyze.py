import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
df = pd.read_csv('imo_2026_medals.csv')

# Handle the typo in 'Continenet'
if 'Continenet' in df.columns:
    df.rename(columns={'Continenet': 'Continent'}, inplace=True)

# Group by continent to get total medals and number of countries
continent_data = df.groupby('Continent').agg(
    G=('G', 'sum'),
    S=('S', 'sum'),
    B=('B', 'sum'),
    HM=('HM', 'sum'),
    Country_Count=('Country', 'count')
).reset_index()

# Calculate per-country averages for each medal type within the continent
for col in ['G', 'S', 'B', 'HM']:
    continent_data[f'Avg_{col}'] = continent_data[col] / continent_data['Country_Count']

# Calculate the average weighted score per country for each continent
# Gold = 5, Silver = 3, Bronze = 1, HM = 0
continent_data['Avg_Score'] = (
    continent_data['Avg_G'] * 5 +
    continent_data['Avg_S'] * 3 +
    continent_data['Avg_B'] * 1
)

# Set up the plot layout
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# 1. Pie Chart - Average Score by Continent
axes[0].pie(continent_data['Avg_Score'], labels=continent_data['Continent'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
axes[0].set_title('Average Relative Performance (Score/Country) by Continent')

# 2. Heatmap - Average Medals per Country by Continent
# Set index to Continent for the heatmap
heatmap_data = continent_data.set_index('Continent')[['Avg_G', 'Avg_S', 'Avg_B', 'Avg_HM']]
sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", ax=axes[1])
axes[1].set_title('Heatmap of Average Medals per Country')
axes[1].set_xlabel('Award Type')
axes[1].set_ylabel('Continent')

plt.tight_layout()
plt.savefig('imo_2026_continent_performance.png')
print("Plots saved to 'imo_2026_continent_performance.png'")
