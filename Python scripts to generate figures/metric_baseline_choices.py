import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    'font.size': 12          # Default text size
})

categories = ["", "No justification provided", "Refer to baseline papers"]
baseline_values = [38, 26, 1]
metric_values = [29, 20, 16]

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
plt.savefig("choice_of_baseline_metrics.pdf")
plt.show()
