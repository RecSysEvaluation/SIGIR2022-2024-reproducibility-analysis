import matplotlib.pyplot as plt
import requests
from pathlib import Path
import pandas as pd


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
data = data.iloc[:45, :]
data = data.iloc[2:, :]
col_to_drop = [0, 2]
data = data.drop(data.columns[[0, 2]], axis = 1)
data = data.T
data.columns = data.iloc[0]
data = data[1:].reset_index(drop=True)


fixed = len( [i for i in data["Embedding size"] if i == "Yes" ]  )
not_fixed = len( [i for i in data["Embedding size"] if i == "No" ]  )
not_reported = len( [i for i in data["Embedding size"] if i != "Yes" and i != "No" ]  )


plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})
# Data
categories = ["Fixed", "Not Fixed", "Not reported"]
values = [fixed, not_fixed, not_reported]

# Plot
colors = ['crimson', 'dodgerblue', 'dodgerblue']
fig, ax = plt.subplots(figsize=(6, 1.5))
bars = ax.barh(categories, values, color=colors)
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


path = Path("Python scripts used to create figures/fig-baselines-fixed-embedding.pdf")
plt.tight_layout()
plt.savefig(path)
plt.show()
