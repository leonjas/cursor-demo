import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from stats import summary_statistics

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Read the CSV file
df = pd.read_csv('student_score.csv')

# Calculate summary statistics
score_list = df['score'].tolist()
summary_stats = summary_statistics(score_list)

# Generate timestamp for file naming
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ===== VISUALIZATION 1: Box Plot with Outlier Analysis =====
plt.figure(figsize=(12, 8))
box_plot = plt.boxplot(df['score'], vert=True, patch_artist=True, 
                       boxprops=dict(facecolor='lightblue', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2),
                       whiskerprops=dict(color='black', linewidth=1.5),
                       capprops=dict(color='black', linewidth=1.5))

# Add statistical annotations
plt.ylabel('SAT Composite Score', fontsize=14, fontweight='bold')
plt.title('SAT Score Distribution - Box Plot Analysis\nShowing Quartiles, Median, and Outliers', 
          fontsize=16, fontweight='bold', pad=20)

# Calculate quartiles for annotation
q1 = np.percentile(df['score'], 25)
q3 = np.percentile(df['score'], 75)
iqr = q3 - q1

# Add text annotations
textstr = '\n'.join([
    f"Q1 (25th percentile): {q1:.0f}",
    f"Median (50th percentile): {summary_stats['median']:.0f}",
    f"Q3 (75th percentile): {q3:.0f}",
    f"IQR: {iqr:.0f}",
    f"Range: {df['score'].min():.0f} - {df['score'].max():.0f}"
])

plt.text(1.15, 0.7, textstr, transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"sat_scores_boxplot_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# ===== VISUALIZATION 2: Violin Plot with Distribution Density =====
plt.figure(figsize=(12, 8))
violin_parts = plt.violinplot(df['score'], vert=True, showmeans=True, showmedians=True)

# Customize colors
for pc in violin_parts['bodies']:
    pc.set_facecolor('lightcoral')
    pc.set_alpha(0.7)

plt.ylabel('SAT Composite Score', fontsize=14, fontweight='bold')
plt.title('SAT Score Distribution - Violin Plot\nShowing Probability Density and Statistical Measures', 
          fontsize=16, fontweight='bold', pad=20)

# Add legend
plt.plot([], [], color='orange', linewidth=2, label='Mean')
plt.plot([], [], color='red', linewidth=2, label='Median')
plt.legend(loc='upper right')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"sat_scores_violin_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# ===== VISUALIZATION 3: Student Ranking Scatter Plot =====
plt.figure(figsize=(14, 10))

# Sort students by score and add ranking
df_sorted = df.sort_values('score', ascending=False).reset_index(drop=True)
df_sorted['rank'] = range(1, len(df_sorted) + 1)

# Create scatter plot
scatter = plt.scatter(df_sorted['rank'], df_sorted['score'], 
                     c=df_sorted['score'], cmap='viridis', 
                     s=60, alpha=0.7, edgecolors='black', linewidth=0.5)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('SAT Score', fontsize=12, fontweight='bold')

# Highlight top 10 and bottom 10 students
top_10 = df_sorted.head(10)
bottom_10 = df_sorted.tail(10)

plt.scatter(top_10['rank'], top_10['score'], s=100, facecolors='none', 
           edgecolors='red', linewidth=2, label='Top 10 Students')
plt.scatter(bottom_10['rank'], bottom_10['score'], s=100, facecolors='none', 
           edgecolors='blue', linewidth=2, label='Bottom 10 Students')

plt.xlabel('Student Rank', fontsize=14, fontweight='bold')
plt.ylabel('SAT Composite Score', fontsize=14, fontweight='bold')
plt.title('Student SAT Score Rankings\nScatter Plot with Performance Tiers', 
          fontsize=16, fontweight='bold', pad=20)

# Add performance percentile lines
plt.axhline(y=np.percentile(df['score'], 90), color='green', linestyle='--', 
           alpha=0.7, label='90th Percentile')
plt.axhline(y=np.percentile(df['score'], 10), color='orange', linestyle='--', 
           alpha=0.7, label='10th Percentile')

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"sat_scores_ranking_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# ===== VISUALIZATION 4: Score Range Categories Bar Chart =====
plt.figure(figsize=(12, 8))

# Define score ranges (common SAT score categories)
score_ranges = {
    'Below Average (1000-1199)': (1000, 1199),
    'Average (1200-1299)': (1200, 1299),
    'Above Average (1300-1399)': (1300, 1399),
    'Excellent (1400-1499)': (1400, 1499),
    'Outstanding (1500-1600)': (1500, 1600)
}

# Count students in each range
range_counts = {}
for range_name, (min_score, max_score) in score_ranges.items():
    count = len(df[(df['score'] >= min_score) & (df['score'] <= max_score)])
    range_counts[range_name] = count

# Create bar chart
bars = plt.bar(range_counts.keys(), range_counts.values(), 
               color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc'],
               edgecolor='black', linewidth=1, alpha=0.8)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')

plt.xlabel('Score Range Categories', fontsize=14, fontweight='bold')
plt.ylabel('Number of Students', fontsize=14, fontweight='bold')
plt.title('Student Distribution Across SAT Score Ranges\nCategorical Performance Analysis', 
          fontsize=16, fontweight='bold', pad=20)

plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f"sat_scores_categories_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# ===== VISUALIZATION 5: Cumulative Distribution Function (CDF) =====
plt.figure(figsize=(12, 8))

# Calculate and plot empirical CDF
sorted_scores = np.sort(df['score'])
y_values = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores)

plt.plot(sorted_scores, y_values, 'b-', linewidth=2, label='Empirical CDF')

# Add percentile lines
percentiles = [10, 25, 50, 75, 90]
colors = ['red', 'orange', 'green', 'purple', 'brown']

for i, p in enumerate(percentiles):
    score_p = np.percentile(df['score'], p)
    plt.axvline(x=score_p, color=colors[i], linestyle='--', alpha=0.7, 
                label=f'{p}th Percentile: {score_p:.0f}')
    plt.axhline(y=p/100, color=colors[i], linestyle='--', alpha=0.7)

plt.xlabel('SAT Composite Score', fontsize=14, fontweight='bold')
plt.ylabel('Cumulative Probability', fontsize=14, fontweight='bold')
plt.title('Cumulative Distribution Function of SAT Scores\nPercentile Analysis', 
          fontsize=16, fontweight='bold', pad=20)

plt.legend(loc='center right')
plt.grid(True, alpha=0.3)
plt.xlim(df['score'].min() - 50, df['score'].max() + 50)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(f"sat_scores_cdf_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# ===== VISUALIZATION 6: Score Distribution Heatmap =====
plt.figure(figsize=(14, 8))

# Create score bins for heatmap
bins = np.arange(1100, 1550, 50)  # 50-point intervals
bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]

# Count students in each bin
bin_counts = []
for i in range(len(bins)-1):
    count = len(df[(df['score'] >= bins[i]) & (df['score'] < bins[i+1])])
    bin_counts.append(count)

# Create a 2D array for heatmap (reshape to show as grid)
heatmap_data = np.array(bin_counts).reshape(1, -1)

# Create heatmap
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', 
            xticklabels=bin_labels, yticklabels=['Student Count'],
            cbar_kws={'label': 'Number of Students'})

plt.title('SAT Score Distribution Heatmap\nStudent Count by Score Ranges', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Score Range', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"sat_scores_heatmap_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print(f"\n=== VISUALIZATION SUMMARY ===")
print(f"Generated {6} different visualizations saved with timestamp: {timestamp}")
print(f"1. Box Plot: sat_scores_boxplot_{timestamp}.png")
print(f"2. Violin Plot: sat_scores_violin_{timestamp}.png") 
print(f"3. Ranking Scatter Plot: sat_scores_ranking_{timestamp}.png")
print(f"4. Score Categories Bar Chart: sat_scores_categories_{timestamp}.png")
print(f"5. Cumulative Distribution Function: sat_scores_cdf_{timestamp}.png")
print(f"6. Score Distribution Heatmap: sat_scores_heatmap_{timestamp}.png")
print(f"\nEach visualization provides different insights:")
print(f"- Box Plot: Shows quartiles, outliers, and spread")
print(f"- Violin Plot: Shows distribution density and shape") 
print(f"- Ranking Scatter: Shows individual student performance ranking")
print(f"- Categories Bar Chart: Shows performance level distribution")
print(f"- CDF Plot: Shows percentile information and cumulative probabilities")
print(f"- Heatmap: Shows concentration of scores in different ranges")