import pandas as pd
import matplotlib.pyplot as plt
from usecase1 import summary_statistics  # Import the function

# Load the data
df = pd.read_csv('student_score.csv')

# Compute summary statistics
stats = summary_statistics(df['score'])
mean = stats['mean']
median = stats['median']
std = stats['std']

# Plot histogram
plt.figure(figsize=(10,6))
plt.hist(df['score'], bins=range(600, 1650, 50), color='skyblue', edgecolor='black')
plt.title('Student SAT Score Distribution in 50 Point Increments')
plt.xlabel('SAT Composite Test Score')
plt.ylabel('Number of Students')
plt.xticks(range(600, 1650, 50), rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate mean, median, std
plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.1f}')
plt.axvline(median, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median:.1f}')
plt.axvline(mean + std, color='purple', linestyle='dotted', linewidth=2, label=f'Std Dev: {std:.1f}')
plt.axvline(mean - std, color='purple', linestyle='dotted', linewidth=2)

# Add legend
plt.legend()

plt.tight_layout()
plt.show()
