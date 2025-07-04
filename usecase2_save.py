import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data
df = pd.read_csv('student_score.csv')

# Plot histogram
plt.figure(figsize=(10,6))
plt.hist(df['score'], bins=range(600, 1650, 50), color='skyblue', edgecolor='black')
plt.title(f'Student SAT Score Distribution in 50 Point Increments\n(Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
plt.xlabel('SAT Composite Test Score')
plt.ylabel('Number of Students')
plt.xticks(range(600, 1650, 50), rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'student_score_histogram_{timestamp}.png'
plt.savefig(filename, dpi=150, bbox_inches='tight')
plt.close()

print(f"Histogram saved as: {filename}")
print(f"Total students: {len(df)}")
print(f"Score range: {df['score'].min()} - {df['score'].max()}")