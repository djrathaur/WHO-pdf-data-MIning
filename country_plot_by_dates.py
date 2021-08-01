"""
Author: Lucas Mendes
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# INPUT VALUES
country = "Brazil"
column = "total_confirmed_new_cases"
title = country + " - Total Confirmed New Cases"

files_folder = "outputs/"
files = [f for f in os.listdir(files_folder) if os.path.isfile(os.path.join(files_folder, f))]

# Begin Code
final_data = pd.DataFrame()

for file in files:
    try:
        data = pd.read_csv(files_folder + file)
        r1 = data.query('country_territory_area == "' + country + '"')
        final_data = final_data.append(r1)
    except:
        print("Error in file reading - " + file)

try:
    plt.interactive(True)
    plt.figure(figsize=(10, 6))
    final_data = final_data.sort_values(by=['date'])
    final_data_plot = sns.barplot(x='date', y=column, data=final_data)

    plt.title(title)
    plt.show(block=True)
except:
    print("Error on trying to plot the result data.")
