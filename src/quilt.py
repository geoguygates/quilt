import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches



def render_quilt(df):
    fig, axs = plt.subplots(4, 3, figsize=(12, 9))
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Iterate over each subplot and draw concentric squares
    for i, ax in enumerate(axs.ravel()):
        sizes, colors = generate_sizes_and_colors(days_in_month[i])
        draw_squares(ax, sizes, colors)
    # Display the plot
    plt.show()


def generate_sizes_and_colors(num_squares):
    # Function to generate sizes and colors for a given number of squares
    sizes = np.linspace(1.0, 0.02, num_squares)
    colormap = plt.cm.coolwarm
    colors = [colormap(i) for i in np.linspace(0, 1, num_squares)]
    return sizes, colors


def draw_squares(ax, sizes, colors):
    # Center of each set of concentric squares within its subplot
    center = (0.5, 0.5)
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    # Function to draw concentric squares on a given axis
    for size, color in zip(sizes, colors):
        lower_left_corner = (center[0] - size / 2, center[1] - size / 2)
        rect = patches.Rectangle(lower_left_corner, size, size, fill=True, color=color)
        ax.add_patch(rect)