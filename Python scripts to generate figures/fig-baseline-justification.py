import matplotlib.pyplot as plt
import requests
from pathlib import Path
import pandas as pd

path = Path("Python scripts to generate figures/google_sheet.csv")
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
    print("Sheet downloaded and saved as 'downloaded_sheet.csv'")
else:
    print("Failed to download. Here's the response:")
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



# Font settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({'font.size': 18})

# Data
categories = ["State-of-the-art", "No justification provided", "Refer to baseline papers"]
values = [38, 26, 1]

# Plot
fig, ax = plt.subplots(figsize=(6, 2))
bars = ax.barh(categories, values, color='dodgerblue')
ax.invert_yaxis()

# Add labels: inside for wide bars, outside for small bars
for bar in bars:
    width = bar.get_width()
    label_x_pos = width / 2 if width > 5 else width + 1  # move label outside if too small
    alignment = 'center' if width > 5 else 'left'
    color = 'white' if width > 5 else 'black'

    ax.text(label_x_pos,
            bar.get_y() + bar.get_height() / 2,
            str(width),
            ha=alignment, va='center',
            color=color)

# Set axis limits
max_val = max(values)
ax.set_xlim(0, max_val + 5)
ax.set_xticks(range(0, max_val + 5, 10))  # start=0, end=max+15, step=5

plt.tight_layout()
plt.savefig("fig-baseline-justification.pdf")
plt.show()
