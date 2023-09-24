import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64



def draw_quilt(config: dict, df: pd.DataFrame):
    # df = read_from_csv(config)
    fig, axs = plt.subplots(4, 3, figsize=(12 , 9))
    
    # calculate your bin size and temperature num_colors
    bin_size = 1 / config['num_colors']
    temp_num_colors = np.linspace(df['tempmax'].min(), df['tempmax'].max(), config['num_colors']+1)

    # Calculate the number of num_colors and create an array representing the num_colors
    num_colors = np.arange(0, 1 + bin_size, bin_size)
    
    # Normalize the temperatures
    normalized_temps = (df['tempmax'] - df['tempmax'].min()) / (df['tempmax'].max() - df['tempmax'].min())
    
    # Generate evenly spaced colors using a colormap
    colormap = plt.cm.coolwarm
    bin_colors = colormap(np.linspace(0, 1, config['num_colors']))
    
    # Bin the normalized temperatures and map them to colors
    bin_indices = np.digitize(normalized_temps, bins=num_colors, right=True)
    colors = bin_colors[bin_indices - 1]
    month_names = ["January", "February", "March", "April","May", "June", "July", "August","September", "October", "November", "December"]

    # Iterate over each subplot and draw concentric squares
    for i, ax in enumerate(axs.ravel()):
        ax.set_aspect('equal', 'box')
        ax.axis('off')
        month_index = i
        monthly_sizes, monthly_colors = __generate_sizes_and_colors_for_a_month(month_index, colors)
        __draw_squares(ax, monthly_sizes, monthly_colors)
        ax.set_title(month_names[month_index], fontsize=10, fontweight='bold')
    
    
    plt.suptitle(f"{config['city']}, {config['state']} - Start Date {config['start_date']}", fontsize=16, fontweight='bold')
    
    # Create a custom legend
    legend_labels = [f'{temp_num_colors[i]:.1f} - {temp_num_colors[i+1]:.1f}°F' for i in range(config['num_colors'])]
    legend_handles = [patches.Patch(color=bin_colors[i], label=legend_labels[i]) for i in range(config['num_colors'])]
    
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left', title='Temperature (°C)')
    
    # Display the plot
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, right=0.8)  # Adjust the layout to make room for the legend and title

    # save the figure to a BytesIO object in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()  # Close the plot to free up memory
    buffer.seek(0)
    
    # Encode in base64 and return
    return 'data:image/png;base64,' + base64.b64encode(buffer.read()).decode()


def __generate_sizes_and_colors_for_a_month(month_index: int, colors: np.array):
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


def __draw_squares(ax, sizes, colors):
    # Center of each set of concentric squares within its subplot
    center = (0.5, 0.5)

    # Function to draw concentric squares on a given axis
    for size, color in zip(sizes, colors):
        lower_left_corner = (center[0] - size / 2, center[1] - size / 2)
        rect = patches.Rectangle(lower_left_corner, size, size, fill=True, color=color)
        ax.add_patch(rect)