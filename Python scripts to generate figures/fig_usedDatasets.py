import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})
# Data
categories = ['Amazon', 'Yelp', 'MovieLens', 'Gowalla', 'Tmall', 'Last.fm', "Retailrocket", 'Others']
values = [28, 23, 22, 20, 11, 6, 6, 74]

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
plt.savefig("fig_usedDatasets.pdf")
plt.show()
