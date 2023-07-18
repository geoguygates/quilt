import matplotlib.pyplot as plt
import numpy as np

# Create a 3 x 4 grid of subplots
fig, axs = plt.subplots(3, 4, figsize=(12, 9))

# Iterate over each subplot
for i in range(3):
    for j in range(4):
        ax = axs[i, j]
        
        # Generate concentric squares representing days of a month
        num_squares = np.random.choice([30, 31])  # Randomly select 30 or 31 squares
        square_sizes = np.arange(1, num_squares + 1)[::-1]
        
        # Plot concentric squares
        ax.pie(square_sizes, colors='white', startangle=90, counterclock=False, wedgeprops={'linewidth': 1, 'edgecolor': 'black'})
        
        # Set aspect ratio to equal for a square plot
        ax.set_aspect('equal')
        
        # Set title as the month
        month = f"Month {i*4 + j + 1}"
        ax.set_title(month)
        
# Adjust spacing between subplots
plt.subplots_adjust(hspace=0.5)

# Show the plot
plt.show()