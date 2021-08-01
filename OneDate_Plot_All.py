
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# INPUT VALUES
csv_file_name = "outputs/" + "20200617-covid-19-sitrep-149.csv"
column = "total_new_deaths"
query = "total_new_deaths >= 25"
title = "Confirmed New Deaths in 17/06/2020\n\n( Query: "+query+" )"

data = pd.read_csv(csv_file_name)

# Plot Results
plt.interactive(True)
plt.figure(figsize=(10, 6))
result1 = data.copy()
result1 = result1.query(query)
result1 = result1.sort_values(by=[column, 'country_territory_area'])
result1_plot = sns.barplot(x='country_territory_area', y=column, data=result1)
result1_plot.set_xticklabels(result1_plot.get_xticklabels(), rotation=60, ha='right')
plt.title(title)

plt.show(block=True)