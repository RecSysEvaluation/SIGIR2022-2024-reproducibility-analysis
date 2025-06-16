import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})
# Data
categories = ['Public dataset(s) used', 'Data filtering information provided', 'Download link provided', 'Preprocessed dataset used', 'Data splits shared']
values = [65, 43, 36, 13, 35]


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
plt.savefig("fig-data-sharing.pdf")
plt.show()
