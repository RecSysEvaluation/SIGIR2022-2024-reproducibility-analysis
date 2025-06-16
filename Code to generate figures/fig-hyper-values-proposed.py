import matplotlib.pyplot as plt

# Font settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({'font.size': 12})

# Data
categories = ["Not reported for any dataset", "Reported for all datasets", "Reported for a subset of datasets"]
values = [38, 25, 2]
colors = ['crimson', 'dodgerblue', 'dodgerblue']
# Plot
fig, ax = plt.subplots(figsize=(6, 1.5))
bars = ax.barh(categories, values, color=colors)
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
ax.set_xlim(0, max_val + 15)
ax.set_xticks(range(0, max_val + 15, 10))  # start=0, end=max+15, step=5

plt.tight_layout()
plt.savefig("fig-hyper-values-proposed.pdf")
plt.show()
