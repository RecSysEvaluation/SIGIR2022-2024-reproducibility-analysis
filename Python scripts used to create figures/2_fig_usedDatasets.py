import matplotlib.pyplot as plt
import requests
from pathlib import Path
import pandas as pd
from collections import defaultdict

path = Path("Python scripts used to create figures/Statistics.csv")
# Correct Sheet ID and GID
sheet_id = "19yPAqB0W1EtANUX3iFP0EE7F5c3EmdLRvu9GR2M9ljs"
gid = "1516783209"
# CSV export URL
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
# Request the CSV
response = requests.get(url)
# Save to file if response is OK
if response.status_code == 200 and "text/csv" in response.headers.get("Content-Type", ""):
    with open(path, "wb") as f:
        f.write(response.content)
    print("Statistics downloaded for the collected papers and saved as 'Statistics.csv'")
else:
    print("Fail to download the statistics of the collected papers. Here's the response:")
    print(response.text[:500])

    
# read data
data = pd.read_csv(path)
used_datasets = data.iloc[58, :]
used_datasets = list(used_datasets[3:])


all_datasets = list()
for str_ in used_datasets:
    str_list = str_.split(",")

    temp = list()
    for i in str_list:
        dataName = i.strip()
        if dataName in ["Amazon-books", "Amazon-baby", "Amazon-sports", "Amazon-cloths", "Amazon-review",
                   "Amazon-beauty", "Amazon-toys", "Amazon cellphones", "Amazon-grocery", "Amazon-automotive", 
                   "Amazon-music", "Amazon-kindle", "Amazon-software", "Amazon-games", "Amazon-bundle", "Amazon", "Amazon-cellphones"]:
            temp.append("Amazons")
        elif dataName in ["MovieLens-10M", "MovieLens", "MovieLens-1M", "MovieLens-25M", "MovieLens-20M", "MovieLens-100k", "MovieLens-1m"]:
            temp.append("MovieLens")
        
        else:
            temp.append(dataName)

        
    temp = list(set(temp))
    all_datasets.append(temp)
        



count_datasets = defaultdict(int)
for dataset_ in all_datasets:

    for dataset in  dataset_:

        if dataset in ["Amazons"]:
            count_datasets["Amazon"] +=1

        elif dataset in ["Yelp"]:
            count_datasets["Yelp"] +=1

        elif dataset in ["MovieLens"]:
            count_datasets["MovieLens"] +=1

        elif dataset in ["Gowalla"]:
            count_datasets["Gowalla"] +=1

        elif dataset in ["Tmall"]:
            count_datasets["Tmall"] +=1

        elif dataset in ["Last.fm"]:
            count_datasets["Last.fm"]+=1
        
        elif dataset in ["Retailrocket"]:
            count_datasets["Retailrocket"] +=1

        else:
            count_datasets["Others"] +=1

    
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})
# Data
categories = ['Amazon', 'Yelp', 'MovieLens', 'Gowalla', 'Tmall', 'Last.fm', "Retailrocket", 'Others']
values = [count_datasets["Amazon"], count_datasets["Yelp"], count_datasets["MovieLens"], 
          count_datasets["Gowalla"], count_datasets["Tmall"], count_datasets["Last.fm"], count_datasets["Retailrocket"], count_datasets["Others"]]

# Sort data by values descending
sorted_data = sorted(zip(values, categories), reverse=True)
sorted_values, sorted_categories = zip(*sorted_data)

# Plot
fig, ax = plt.subplots(figsize=(6, 2.5))
bars = ax.barh(categories, values, color='dodgerblue')
ax.invert_yaxis()
# Flip the y-axis so largest value is at the top

# Add values inside bars
for bar in bars:
    width = bar.get_width()
    ax.text(width / 2,                       # x = middle of the bar
            bar.get_y() + bar.get_height()/2,  # y = middle of the bar
            str(width),                      # label text
            ha='center', va='center',        # horizontal and vertical align center
            color='white')       # adjust font size/color as needed

# Labels and styling
ax.set_xlim(0, max(values) + 10)

plt.tight_layout()

path = Path("Python scripts used to create figures/fig_usedDatasets.pdf")
plt.savefig(path)
plt.show()
