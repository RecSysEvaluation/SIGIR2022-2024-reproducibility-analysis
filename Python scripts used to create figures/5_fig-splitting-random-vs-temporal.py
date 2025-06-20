import matplotlib.pyplot as plt
import requests
from pathlib import Path
import pandas as pd
from collections import defaultdict

plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})

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
data = data.iloc[:41, :]
data = data.iloc[2:, :]
col_to_drop = [0, 2]
data = data.drop(data.columns[[0, 2]], axis = 1)
data = data.T
data.columns = data.iloc[0]
data = data[1:].reset_index(drop=True)


refer_baselines = len( [i for i in data["Evaluation procedure"] if i == "Refer to baselines" ]  )


all_evaluation_measures = list()
for str_ in data["Evaluation procedure"]:
    str_list = str_.split(",")

    temp = list()
    for i in str_list:
        temp.append(i.strip())
    temp = list(set(temp))
    all_evaluation_measures.append(temp)

count_dict = defaultdict(int)
for eval_per_paper in all_evaluation_measures:
    for i in eval_per_paper:
        
        if i == "Splitting after time-based sorting":
          count_dict["splitting_after_time_based_sorting"] +=1 
        
        if i == "No detail on temporal or random splitting":
          count_dict["no_detail_on_temporal_or_random_splitting"] +=1

        if i == "Random splitting":
          count_dict["random_splitting"] +=1   

        if i == "Not reported":
          count_dict["not_reported"] +=1

        



# Data
categories = ['Splitting after time-based sorting', 'No detail on temporal or random splitting', 'Random splitting', 'Refer to baselines', 'No information about splitting provided']
values = [count_dict["splitting_after_time_based_sorting"], count_dict["no_detail_on_temporal_or_random_splitting"], 
          count_dict["random_splitting"], refer_baselines, count_dict["not_reported"]]

# Sort data by values descending
sorted_data = sorted(zip(values, categories), reverse=True)
sorted_values, sorted_categories = zip(*sorted_data)

# Plot
fig, ax = plt.subplots(figsize=(6, 2))
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
max_val = max(values)
ax.set_xlim(0, max_val + 10)
ax.set_xticks(range(0, max_val + 10, 10))  # start=0, end=max+15, step=5



plt.tight_layout()
path = Path("Python scripts used to create figures/fig-splitting-random-vs-temporal.pdf")
plt.savefig(path)
plt.show()
