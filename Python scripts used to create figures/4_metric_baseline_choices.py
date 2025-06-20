import matplotlib.pyplot as plt
import requests
from pathlib import Path
import pandas as pd
import numpy as np


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




# baselines.....
baseline_state_of_the_art = len( [i for i in data["Choice of baselines"] if i == "State-of-the-art" ]  )
baseline_no_justification_provided = len( [i for i in data["Choice of baselines"] if i == "No justification provided" ]  )
baseline_refer_to_baseline_papers = len( [i for i in data["Choice of baselines"] if i == "Refer to baseline papers" ]  )

# metric values.............
metrics_popularity_based = len( [i for i in data["Choice of metrics"] if i == "Popularity" ]  )
metrics_no_justification_provided = len( [i for i in data["Choice of metrics"] if i == "No justification provided" ]  )
metrics_refer_to_baseline_papers = len( [i for i in data["Choice of metrics"] if i == "Refer to baseline papers" ]  )

categories = ["", "No justification provided", "Refer to baseline papers"]
baseline_values = [baseline_state_of_the_art, baseline_no_justification_provided, baseline_refer_to_baseline_papers]
metric_values = [metrics_popularity_based, metrics_no_justification_provided, metrics_refer_to_baseline_papers]

# Bar position and width
x = np.arange(len(categories))
width = 0.35  # Thickness of each bar

# Plot setup
fig, ax = plt.subplots(figsize=(6, 3))

# Bars
bars1 = ax.barh(x - width/2, baseline_values, height=width, label='Choice of Baselines', color='#F4B400')
bars2 = ax.barh(x + width/2, metric_values, height=width, label='Choice of Used Metrics', color='#DB4437')

# Axis labels and title
ax.set_xlabel('Number of Papers')
#ax.set_title('Justification of Experimental Design')
ax.set_yticks(x)
ax.set_yticklabels(categories)
ax.invert_yaxis()  # So the highest value is at the top
ax.legend()
# Add values next to bars
        
for bar in bars1 + bars2:
    width = bar.get_width()
    if width < 5:
        ax.text(width + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f'{int(width)}',
                ha='left', va='center',
                color='black')
    else:
        ax.text(width * 0.5,
                bar.get_y() + bar.get_height() / 2,
                f'{int(width)}',
                ha='center', va='center',
                color='white')
        
# Get the bar positions directly
first_bar_baseline = bars1[0]
first_bar_metric = bars2[0]

# Add custom labels on the left side of the first bar group
ax.text(-1, 
        first_bar_baseline.get_y() + first_bar_baseline.get_height()/2,
        "State-of-the-art",
        va='center', ha='right')

ax.text(-1,
        first_bar_metric.get_y() + first_bar_metric.get_height()/2,
        "Popularity-based",
        va='center', ha='right')


# Layout improvements
ax.set_xlim(0, max(baseline_values) + 15)
plt.subplots_adjust(left=0.3)

plt.tight_layout()
path = Path("Python scripts used to create figures/choice_of_baseline_metrics.pdf")
plt.savefig(path)
plt.show()
