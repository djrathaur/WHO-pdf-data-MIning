

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# INPUT VALUES
column = "total_confirmed_new_cases"
title = "World " + column

dataset_file = "covid-full-dataset.csv"

# Begin Code
final_data = pd.DataFrame()

data = pd.read_csv(dataset_file)

query_data = data[(data['country_territory_area'] != 'Grandtotal')]
query_data = query_data[(query_data['country_territory_area'] != 'Subtotalforallregions')]
query_data = query_data[(query_data['country_territory_area'] != 'Regions')]
query_data = query_data[(query_data['country_territory_area'] != 'America')]
query_data = query_data[(query_data['country_territory_area'] != 'Subtotalforall')]
query_data = query_data[(query_data['total_confirmed_cases'] != 0)]
query_data = query_data[(query_data['total_confirmed_new_cases'] != 0)]
#newData = query_data[(query_data['date'] == '2020/05/31' )]
query_data = query_data.groupby(['date'])[column].sum().reset_index()
query_data = query_data[(query_data['date'] != '2020/01/01')]
query_data = query_data[query_data[column] >= 1000]

#print(newData[newData[column] == newData[column].max()].head(5).to_string())

try:
    plt.interactive(True)
    plt.figure(figsize=(60, 20))
    sns.set_style("whitegrid")
    plt.locator_params(axis='y', nbins=14)

    #query_data = query_data.sort_values(by=['date'])
    final_data_plot = sns.barplot(x='date', y=column, data=query_data)

    final_data_plot.set_xlabel(column, fontsize=25)
    final_data_plot.set_ylabel("Date (Year/Month/Day)", fontsize=25)

    final_data_plot.set_xticklabels(final_data_plot.get_xticklabels(), rotation=60, ha='right', fontsize=16)
    final_data_plot.set_yticklabels(final_data_plot.get_yticks(), size=20, )

    plt.title(title, fontsize=45, pad=20)
    plt.show(block=True)
    #final_data_plot.figure.savefig("dataset_query_output.png")

except:
    print("Error on trying to plot the result data.")
