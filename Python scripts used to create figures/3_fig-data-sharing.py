import matplotlib.pyplot as plt
import requests
from pathlib import Path
import pandas as pd

path = Path("Python scripts used to create figuresStatistics.csv")
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



public_dataset_used = len( [i for i in data["Public dataset"] if i == "Yes" ]  )
data_filtering_information_provided = len( [i for i in data["Data filtering"] if i != "Not provided" ]  )
download_link_provided = len( [i for i in data["Downloadable dataset"] if i != "Not provided for any dataset" ]  )
preprocessed_datasets_provided = len( [i for i in data["Preprocessed dataset"] if i != "Not provided for any dataset" ]  )
data_split_shared = len( [i for i in data["Data splits"] if i != "Not provided for any dataset" ]  )


# Count cases for which authors did not provide any link.......

temp1 = list(data["Downloadable dataset"])
temp2 = list(data["Preprocessed dataset"])
temp3 = list(data["Data splits"])
count = 0
for i in range(len(data["Downloadable dataset"])):
    if temp1[i] == "Not provided for any dataset" and temp2[i] == "Not provided for any dataset" and temp3[i] == "Not provided for any dataset":
        count +=1


print("Number of papers for which the authors did not provide any link: "+str(count))



plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})
# Data
categories = ['Public dataset(s) used', 'Data filtering information provided', 'Download link provided', 'Preprocessed dataset used', 'Data splits shared']
values = [public_dataset_used,  data_filtering_information_provided,  download_link_provided,  preprocessed_datasets_provided,  data_split_shared]


# Plot
fig, ax = plt.subplots(figsize=(6, 2))
bars = ax.barh(categories, values, color='dodgerblue')
ax.invert_yaxis()
#ax.invert_yaxis()
# Flip the y-axis so largest value is at the top

# Add values inside bars
for bar in bars:
    width = bar.get_width()
    ax.text(width / 2,                       # x = middle of the bar
            bar.get_y() + bar.get_height()/2,  # y = middle of the bar
            str(width),                      # label text
            ha='center', va='center',        # horizontal and vertical align center
            color='white')       # adjust font size/color as needed

max_val = max(values)
ax.set_xlim(0, max_val + 10)
ax.set_xticks(range(0, max_val + 10, 10))  # start=0, end=max+15, step=5

plt.tight_layout()
path = Path("Python scripts used to create figures/fig-data-sharing.pdf")
plt.savefig(path)
plt.show()
