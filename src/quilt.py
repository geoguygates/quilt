import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils import Reader



def draw_quilt(config):
    df = Reader(config).read_from_csv()
    fig, axs = plt.subplots(4, 3, figsize=(12 , 9))
    
    # calculate your bin size
    bin_size = 1/config['bins']

    # Calculate the number of bins and create an array representing the bins
    bins = np.arange(0, 1 + bin_size, bin_size)
    
    # Normalize the temperatures
    normalized_temps = (df['tempmax'] - df['tempmax'].min()) / (df['tempmax'].max() - df['tempmax'].min())
    
    # Generate evenly spaced colors using a colormap
    colormap = plt.cm.coolwarm
    bin_colors = colormap(np.linspace(0, 1, config['bins']))
    
    # Bin the normalized temperatures and map them to colors
    bin_indices = np.digitize(normalized_temps, bins=bins, right=True)
    colors = bin_colors[bin_indices - 1]
    month_names = ["January", "February", "March", "April","May", "June", "July", "August","September", "October", "November", "December"]

    # Iterate over each subplot and draw concentric squares
    for i, ax in enumerate(axs.ravel()):
        month_index = i
        monthly_sizes, monthly_colors = generate_sizes_and_colors_for_a_month(df, month_index, colors)
        draw_squares(ax, monthly_sizes, monthly_colors)
        ax.set_title(month_names[month_index], fontsize=10, fontweight='bold')
    
    
    plt.suptitle(f"{config['city']}, {config['state']} - {config['year']}", fontsize=16, fontweight='bold')
    # Display the plot
    return plt.show()


def generate_sizes_and_colors_for_a_month(df, month_index: int, colors: np.array):
    # Function to generate sizes and colors for a given number of squares
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Calculating the start index dynamically based on the month_index
    start_idx = sum(days_in_month[:month_index])
    
    # Getting the number of days in the selected month
    days = days_in_month[month_index]
    sizes = np.linspace(1.0, 0.02, days)

    # Calculating the end index
    end_idx = start_idx + days
        
    # Getting the subset of the data array
    monthly_colors = colors[start_idx:end_idx]
    
    return sizes, monthly_colors


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