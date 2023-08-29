import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Define the figure and a 3x4 grid of subplots
fig, axs = plt.subplots(4, 3, figsize=(12, 9))

# Center of each set of concentric squares within its subplot
center = (0.5, 0.5)

# Generate 30 sizes using linspace from 0.02 to 1.0 (small to large)
sizes = np.linspace(1.0, 0.02, 30)

# Use a colormap to get 30 colors
colormap = plt.cm.viridis
colors = [colormap(i) for i in np.linspace(0, 1, 30)]

# Function to draw concentric squares on a given axis
def draw_squares(ax):
    for size, color in zip(sizes, colors):
        lower_left_corner = (center[0] - size / 2, center[1] - size / 2)
        rect = patches.Rectangle(lower_left_corner, size, size, fill=True, color=color)
        ax.add_patch(rect)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', 'box')
    ax.axis('off')  # Hide axis

# Iterate over each subplot and draw concentric squares
for ax in axs.ravel():
    draw_squares(ax)

plt.tight_layout()
plt.show()