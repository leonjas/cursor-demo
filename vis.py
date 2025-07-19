import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from stats import summary_statistics

# Read the CSV file
df = pd.read_csv('student_score.csv')

# Calculate summary statistics using our custom function
score_list = df['score'].tolist()
summary_stats = summary_statistics(score_list)

# Set up the figure and axis
plt.figure(figsize=(14, 8))

# Create bins for the histogram in 50 point increments
bins = np.arange(600, 1651, 50)

# Create the histogram and get the data for fitting
n, bins_edges, patches = plt.hist(
    df['score'], 
    bins=bins, 
    density=True,  # Use density for proper PDF overlay
    edgecolor='black', 
    alpha=0.7,
    color='lightblue',
    label='SAT Score Distribution'
)

# Generate x values for the normal distribution curve
x = np.linspace(600, 1650, 100)

# Create normal distribution using our calculated mean and std
normal_dist = stats.norm(summary_stats['mean'], summary_stats['std'])
y = normal_dist.pdf(x)

# Plot the normal distribution curve
plt.plot(x, y, 'r-', linewidth=2, label='Normal Distribution Fit')

# Add vertical lines for mean and median with annotations
plt.axvline(
    summary_stats['mean'], 
    color='red', 
    linestyle='--', 
    linewidth=2, 
    alpha=0.8,
    label=f"Mean: {summary_stats['mean']:.1f}"
)
plt.axvline(
    summary_stats['median'], 
    color='green', 
    linestyle='--', 
    linewidth=2, 
    alpha=0.8,
    label=f"Median: {summary_stats['median']:.1f}"
)

# Add text annotations for statistics
textstr = '\n'.join([
    f"Mean: {summary_stats['mean']:.1f}",
    f"Median: {summary_stats['median']:.1f}",
    f"Std Dev: {summary_stats['std']:.1f}",
    f"Sample Size: {summary_stats['count']}"
])

# Place the text box in the upper right corner
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
plt.text(
    0.98, 0.98, textstr, transform=plt.gca().transAxes, fontsize=11,
    verticalalignment='top', horizontalalignment='right', bbox=props
)

# Set enhanced labels and title
plt.xlabel('SAT Composite Score', fontsize=14, fontweight='bold')
plt.ylabel('Probability Density', fontsize=14, fontweight='bold')
plt.title(
    'Distribution of SAT Composite Scores with Statistical Analysis\n'
    'Histogram with Normal Distribution Overlay', 
    fontsize=16, 
    fontweight='bold',
    pad=20
)

# Add legend
plt.legend(loc='upper left', fontsize=11)

# Add gridlines for better readability
plt.grid(True, linestyle='--', alpha=0.3)

# Set x-axis limits and ticks
plt.xlim(600, 1650)
plt.xticks(bins, rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot with timestamp
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"student_scores_visualization_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Visualization saved as: {filename}")

# Display the plot on screen
plt.show()

# Close the plot to free memory
plt.close()
