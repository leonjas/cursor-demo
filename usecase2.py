import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('student_score.csv')

# Plot histogram
plt.figure(figsize=(10,6))
plt.hist(df['score'], bins=range(600, 1650, 50), color='skyblue', edgecolor='black')
plt.title('Student SAT Score Distribution in 50 Point Increments')
plt.xlabel('SAT Composite Test Score')
plt.ylabel('Number of Students')
plt.xticks(range(600, 1650, 50), rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
