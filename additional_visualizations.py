import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm, probplot
import seaborn as sns
from stats import summary_statistics
from datetime import datetime

# Set the style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Read the CSV file
df = pd.read_csv('student_score.csv')
scores = df['score'].tolist()
summary_stats = summary_statistics(scores)

# Create timestamp for file naming
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("Generating multiple visualizations for student scores...")
print(f"Dataset contains {len(scores)} student scores")
print(f"Score range: {summary_stats['min']} - {summary_stats['max']}")

# ================================================================
# 1. BOX PLOT WITH QUARTILE ANALYSIS
# ================================================================
plt.figure(figsize=(12, 8))
box_plot = plt.boxplot(scores, patch_artist=True, notch=True, vert=True)

# Customize the box plot
box_plot['boxes'][0].set_facecolor('lightblue')
box_plot['boxes'][0].set_alpha(0.7)

# Add statistical annotations
q1 = np.percentile(scores, 25)
q3 = np.percentile(scores, 75)
iqr = q3 - q1

plt.text(1.15, summary_stats['median'], f"Median: {summary_stats['median']:.0f}", 
         verticalalignment='center', fontweight='bold')
plt.text(1.15, q1, f"Q1: {q1:.0f}", verticalalignment='center')
plt.text(1.15, q3, f"Q3: {q3:.0f}", verticalalignment='center')
plt.text(1.15, summary_stats['min'], f"Min: {summary_stats['min']:.0f}", 
         verticalalignment='center')
plt.text(1.15, summary_stats['max'], f"Max: {summary_stats['max']:.0f}", 
         verticalalignment='center')

plt.ylabel('SAT Score', fontsize=12, fontweight='bold')
plt.title('SAT Score Distribution - Box Plot Analysis\nQuartiles, Median, and Outlier Detection', 
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.tight_layout()

filename = f"boxplot_analysis_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Box plot saved as: {filename}")
plt.close()

# ================================================================
# 2. VIOLIN PLOT - DENSITY + BOX PLOT COMBINED
# ================================================================
plt.figure(figsize=(12, 8))
violin_parts = plt.violinplot(scores, positions=[1], showmeans=True, showmedians=True)

# Customize violin plot colors
for pc in violin_parts['bodies']:
    pc.set_facecolor('lightgreen')
    pc.set_alpha(0.7)

plt.ylabel('SAT Score', fontsize=12, fontweight='bold')
plt.title('SAT Score Distribution - Violin Plot\nDensity Distribution with Quartile Information', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks([1], ['All Students'])
plt.grid(True, alpha=0.3)
plt.tight_layout()

filename = f"violin_plot_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Violin plot saved as: {filename}")
plt.close()

# ================================================================
# 3. SCATTER PLOT WITH STUDENT INDEX AND TREND LINE
# ================================================================
plt.figure(figsize=(14, 8))
student_indices = range(1, len(scores) + 1)

plt.scatter(student_indices, scores, alpha=0.7, s=60, c='steelblue', edgecolors='black', linewidth=0.5)

# Add trend line
z = np.polyfit(student_indices, scores, 1)
p = np.poly1d(z)
plt.plot(student_indices, p(student_indices), "r--", linewidth=2, alpha=0.8, 
         label=f'Trend line (slope: {z[0]:.2f})')

# Add horizontal line for mean
plt.axhline(y=summary_stats['mean'], color='orange', linestyle='-', linewidth=2, 
           alpha=0.8, label=f"Mean: {summary_stats['mean']:.1f}")

plt.xlabel('Student Index (Order in Dataset)', fontsize=12, fontweight='bold')
plt.ylabel('SAT Score', fontsize=12, fontweight='bold')
plt.title('SAT Scores by Student Index\nExploring Patterns in Data Collection Order', 
          fontsize=14, fontweight='bold', pad=20)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

filename = f"scatter_index_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Scatter plot with trend saved as: {filename}")
plt.close()

# ================================================================
# 4. BAR CHART OF SCORE RANGES
# ================================================================
plt.figure(figsize=(14, 8))

# Define score ranges
ranges = [(1200, 1299), (1300, 1399), (1400, 1499), (1500, 1600)]
range_labels = ['1200-1299\n(Good)', '1300-1399\n(Very Good)', '1400-1499\n(Excellent)', '1500-1600\n(Outstanding)']
range_counts = []
range_colors = ['lightcoral', 'lightskyblue', 'lightgreen', 'gold']

for low, high in ranges:
    count = sum(1 for score in scores if low <= score <= high)
    range_counts.append(count)

# Add scores below 1200 if any exist
below_1200 = sum(1 for score in scores if score < 1200)
if below_1200 > 0:
    range_labels.insert(0, 'Below 1200\n(Needs Improvement)')
    range_counts.insert(0, below_1200)
    range_colors.insert(0, 'lightgray')

bars = plt.bar(range_labels, range_counts, color=range_colors, edgecolor='black', linewidth=1, alpha=0.8)

# Add value labels on bars
for bar, count in zip(bars, range_counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{count}\n({count/len(scores)*100:.1f}%)', 
             ha='center', va='bottom', fontweight='bold')

plt.ylabel('Number of Students', fontsize=12, fontweight='bold')
plt.xlabel('Score Ranges', fontsize=12, fontweight='bold')
plt.title('Distribution of Students Across SAT Score Ranges\nPerformance Categories', 
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()

filename = f"score_ranges_bar_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Score ranges bar chart saved as: {filename}")
plt.close()

# ================================================================
# 5. CUMULATIVE DISTRIBUTION FUNCTION (CDF)
# ================================================================
plt.figure(figsize=(14, 8))

# Calculate empirical CDF
sorted_scores = np.sort(scores)
cumulative_prob = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores)

plt.plot(sorted_scores, cumulative_prob, 'b-', linewidth=3, label='Empirical CDF', alpha=0.8)

# Add theoretical normal CDF for comparison
x_norm = np.linspace(min(scores), max(scores), 100)
normal_cdf = norm.cdf(x_norm, summary_stats['mean'], summary_stats['std'])
plt.plot(x_norm, normal_cdf, 'r--', linewidth=2, label='Normal Distribution CDF', alpha=0.8)

# Add percentile lines
percentiles = [25, 50, 75, 90, 95]
for p in percentiles:
    score_at_p = np.percentile(scores, p)
    plt.axvline(score_at_p, color='gray', linestyle=':', alpha=0.6)
    plt.text(score_at_p, 0.05, f'{p}th\n{score_at_p:.0f}', 
             rotation=90, verticalalignment='bottom', horizontalalignment='center')

plt.xlabel('SAT Score', fontsize=12, fontweight='bold')
plt.ylabel('Cumulative Probability', fontsize=12, fontweight='bold')
plt.title('Cumulative Distribution Function of SAT Scores\nEmpirical vs Normal Distribution', 
          fontsize=14, fontweight='bold', pad=20)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

filename = f"cdf_plot_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"CDF plot saved as: {filename}")
plt.close()

# ================================================================
# 6. Q-Q PLOT FOR NORMALITY TESTING
# ================================================================
plt.figure(figsize=(12, 8))

# Create Q-Q plot
(osm, osr), (slope, intercept, r_value) = probplot(scores, dist="norm", plot=plt)

plt.title('Q-Q Plot: Testing Normality of SAT Scores\n' + 
          f'R² = {r_value**2:.4f} (closer to 1.0 indicates more normal distribution)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Theoretical Quantiles (Normal Distribution)', fontsize=12, fontweight='bold')
plt.ylabel('Sample Quantiles (Actual Scores)', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()

filename = f"qq_plot_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Q-Q plot saved as: {filename}")
plt.close()

# ================================================================
# 7. PERCENTILE RANKING VISUALIZATION
# ================================================================
plt.figure(figsize=(14, 10))

# Calculate percentile ranks for each student
percentile_ranks = []
for score in scores:
    rank = sum(1 for s in scores if s <= score) / len(scores) * 100
    percentile_ranks.append(rank)

# Create a horizontal bar chart of top and bottom performers
df_with_percentiles = pd.DataFrame({
    'name': df['name'],
    'score': df['score'],
    'percentile': percentile_ranks
})

# Sort by score and take top 10 and bottom 10
df_sorted = df_with_percentiles.sort_values('score')
top_bottom = pd.concat([df_sorted.head(10), df_sorted.tail(10)])

# Create the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

# Bottom 10 performers
bottom_10 = df_sorted.head(10)
bars1 = ax1.barh(range(len(bottom_10)), bottom_10['score'], 
                color='lightcoral', alpha=0.8, edgecolor='black')
ax1.set_yticks(range(len(bottom_10)))
ax1.set_yticklabels(bottom_10['name'], fontsize=10)
ax1.set_xlabel('SAT Score', fontsize=12, fontweight='bold')
ax1.set_title('Bottom 10 Performers', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Add score labels
for i, (score, percentile) in enumerate(zip(bottom_10['score'], bottom_10['percentile'])):
    ax1.text(score + 10, i, f'{score}\n({percentile:.1f}%ile)', 
             va='center', fontweight='bold', fontsize=9)

# Top 10 performers
top_10 = df_sorted.tail(10)
bars2 = ax2.barh(range(len(top_10)), top_10['score'], 
                color='lightgreen', alpha=0.8, edgecolor='black')
ax2.set_yticks(range(len(top_10)))
ax2.set_yticklabels(top_10['name'], fontsize=10)
ax2.set_xlabel('SAT Score', fontsize=12, fontweight='bold')
ax2.set_title('Top 10 Performers', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Add score labels
for i, (score, percentile) in enumerate(zip(top_10['score'], top_10['percentile'])):
    ax2.text(score + 10, i, f'{score}\n({percentile:.1f}%ile)', 
             va='center', fontweight='bold', fontsize=9)

plt.suptitle('SAT Score Performance Rankings\nTop and Bottom Performers with Percentile Ranks', 
             fontsize=16, fontweight='bold')
plt.tight_layout()

filename = f"percentile_rankings_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Percentile rankings saved as: {filename}")
plt.close()

# ================================================================
# 8. PIE CHART OF PERFORMANCE CATEGORIES
# ================================================================
plt.figure(figsize=(12, 8))

# Define performance categories based on typical SAT score interpretations
categories = {
    'Outstanding (1500+)': sum(1 for s in scores if s >= 1500),
    'Excellent (1400-1499)': sum(1 for s in scores if 1400 <= s < 1500),
    'Very Good (1300-1399)': sum(1 for s in scores if 1300 <= s < 1400),
    'Good (1200-1299)': sum(1 for s in scores if 1200 <= s < 1300),
    'Below Average (<1200)': sum(1 for s in scores if s < 1200)
}

# Remove categories with 0 students
categories = {k: v for k, v in categories.items() if v > 0}

colors = ['gold', 'lightgreen', 'lightskyblue', 'lightcoral', 'lightgray']
colors = colors[:len(categories)]

# Create pie chart
wedges, texts, autotexts = plt.pie(categories.values(), labels=categories.keys(), 
                                  autopct='%1.1f%%', colors=colors, startangle=90,
                                  explode=[0.05] * len(categories))

# Enhance text formatting
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

for text in texts:
    text.set_fontsize(10)
    text.set_fontweight('bold')

plt.title('Distribution of SAT Performance Categories\nPercentage of Students in Each Performance Level', 
          fontsize=14, fontweight='bold', pad=20)

# Add a summary box
summary_text = f"Total Students: {len(scores)}\nMean Score: {summary_stats['mean']:.1f}\nStd Dev: {summary_stats['std']:.1f}"
plt.text(1.3, 0, summary_text, fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat"))

plt.axis('equal')
plt.tight_layout()

filename = f"performance_categories_pie_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Performance categories pie chart saved as: {filename}")
plt.close()

print(f"\n✅ All visualizations completed and saved!")
print(f"Generated 8 different visualization types:")
print(f"1. Box Plot Analysis - {filename.replace('performance_categories_pie', 'boxplot_analysis')}")
print(f"2. Violin Plot - {filename.replace('performance_categories_pie', 'violin_plot')}")
print(f"3. Scatter Plot with Trend - {filename.replace('performance_categories_pie', 'scatter_index')}")
print(f"4. Score Ranges Bar Chart - {filename.replace('performance_categories_pie', 'score_ranges_bar')}")
print(f"5. Cumulative Distribution Function - {filename.replace('performance_categories_pie', 'cdf_plot')}")
print(f"6. Q-Q Plot for Normality - {filename.replace('performance_categories_pie', 'qq_plot')}")
print(f"7. Percentile Rankings - {filename.replace('performance_categories_pie', 'percentile_rankings')}")
print(f"8. Performance Categories Pie Chart - {filename}")