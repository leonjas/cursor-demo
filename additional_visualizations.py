import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Read the CSV file
df = pd.read_csv('student_score.csv')

# Create timestamp for file naming
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 1. BOX PLOT - Shows quartiles, median, and outliers
plt.figure(figsize=(10, 8))
box_plot = plt.boxplot(df['score'], patch_artist=True, 
                      boxprops=dict(facecolor='lightblue', alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      whiskerprops=dict(color='darkblue', linewidth=2),
                      capprops=dict(color='darkblue', linewidth=2))

plt.ylabel('SAT Score', fontsize=14, fontweight='bold')
plt.title('SAT Score Distribution - Box Plot\nShowing Quartiles, Median, and Outliers', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)

# Add statistical annotations
q1 = df['score'].quantile(0.25)
q2 = df['score'].median()
q3 = df['score'].quantile(0.75)
iqr = q3 - q1

stats_text = f"Q1: {q1:.0f}\nMedian: {q2:.0f}\nQ3: {q3:.0f}\nIQR: {iqr:.0f}"
plt.text(1.15, q2, stats_text, fontsize=12, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))

plt.tight_layout()
plt.savefig(f"boxplot_scores_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 2. VIOLIN PLOT - Shows distribution shape more smoothly
plt.figure(figsize=(10, 8))
violin_parts = plt.violinplot(df['score'], positions=[1], showmeans=True, showmedians=True)

# Customize violin plot colors
for pc in violin_parts['bodies']:
    pc.set_facecolor('lightcoral')
    pc.set_alpha(0.7)

plt.ylabel('SAT Score', fontsize=14, fontweight='bold')
plt.title('SAT Score Distribution - Violin Plot\nShowing Distribution Shape and Density', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.xticks([1], ['All Students'])

plt.tight_layout()
plt.savefig(f"violin_plot_scores_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 3. SCORE RANGES BAR CHART
plt.figure(figsize=(12, 8))

# Define score ranges
bins = [1100, 1200, 1300, 1400, 1500, 1600]
labels = ['1100-1199', '1200-1299', '1300-1399', '1400-1499', '1500+']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

# Create score range categories
df['score_range'] = pd.cut(df['score'], bins=bins, labels=labels, right=False)
range_counts = df['score_range'].value_counts().sort_index()

bars = plt.bar(range_counts.index, range_counts.values, color=colors, alpha=0.8, edgecolor='black')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')

plt.xlabel('Score Range', fontsize=14, fontweight='bold')
plt.ylabel('Number of Students', fontsize=14, fontweight='bold')
plt.title('Distribution of Students by Score Range\nFrequency Count per Range', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3, axis='y')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(f"score_ranges_bar_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 4. CUMULATIVE DISTRIBUTION FUNCTION (CDF)
plt.figure(figsize=(12, 8))

# Calculate CDF
sorted_scores = np.sort(df['score'])
cumulative_prob = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores)

plt.plot(sorted_scores, cumulative_prob, linewidth=3, color='purple', label='Empirical CDF')

# Add theoretical normal CDF for comparison
mean_score = df['score'].mean()
std_score = df['score'].std()
x_norm = np.linspace(sorted_scores.min(), sorted_scores.max(), 100)
y_norm = stats.norm.cdf(x_norm, mean_score, std_score)
plt.plot(x_norm, y_norm, '--', linewidth=2, color='orange', label='Normal CDF')

# Add percentile lines
percentiles = [25, 50, 75]
for p in percentiles:
    score_at_p = np.percentile(df['score'], p)
    plt.axvline(score_at_p, color='red', linestyle=':', alpha=0.7)
    plt.axhline(p/100, color='red', linestyle=':', alpha=0.7)
    plt.text(score_at_p + 10, p/100 + 0.02, f'{p}th percentile\n({score_at_p:.0f})', 
             fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

plt.xlabel('SAT Score', fontsize=14, fontweight='bold')
plt.ylabel('Cumulative Probability', fontsize=14, fontweight='bold')
plt.title('Cumulative Distribution Function of SAT Scores\nShowing Percentiles and Normal Comparison', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

plt.tight_layout()
plt.savefig(f"cdf_scores_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 5. KERNEL DENSITY ESTIMATION (KDE) PLOT
plt.figure(figsize=(12, 8))

# Create KDE plot
kde_data = df['score']
kde = stats.gaussian_kde(kde_data)
x_range = np.linspace(kde_data.min() - 50, kde_data.max() + 50, 200)
kde_values = kde(x_range)

plt.fill_between(x_range, kde_values, alpha=0.6, color='lightgreen', label='KDE')
plt.plot(x_range, kde_values, color='darkgreen', linewidth=2)

# Add rug plot (individual data points)
plt.plot(kde_data, np.zeros(len(kde_data)), '|', color='red', alpha=0.8, markersize=10, label='Individual Scores')

# Add mean and std lines
mean_score = kde_data.mean()
std_score = kde_data.std()
plt.axvline(mean_score, color='blue', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.1f}')
plt.axvline(mean_score + std_score, color='orange', linestyle=':', alpha=0.7, label=f'+1 SD: {mean_score + std_score:.1f}')
plt.axvline(mean_score - std_score, color='orange', linestyle=':', alpha=0.7, label=f'-1 SD: {mean_score - std_score:.1f}')

plt.xlabel('SAT Score', fontsize=14, fontweight='bold')
plt.ylabel('Density', fontsize=14, fontweight='bold')
plt.title('Kernel Density Estimation of SAT Scores\nSmooth Distribution with Individual Data Points', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

plt.tight_layout()
plt.savefig(f"kde_scores_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 6. PERFORMANCE GRADES PIE CHART
plt.figure(figsize=(10, 10))

# Define grade categories based on typical SAT score ranges
def assign_grade(score):
    if score >= 1400:
        return 'Excellent (1400+)'
    elif score >= 1300:
        return 'Good (1300-1399)'
    elif score >= 1200:
        return 'Average (1200-1299)'
    else:
        return 'Below Average (<1200)'

df['grade'] = df['score'].apply(assign_grade)
grade_counts = df['grade'].value_counts()

colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
explode = (0.05, 0.05, 0.05, 0.05)  # slightly separate all slices

wedges, texts, autotexts = plt.pie(grade_counts.values, labels=grade_counts.index, 
                                  autopct='%1.1f%%', startangle=90, colors=colors, 
                                  explode=explode, shadow=True)

# Enhance text formatting
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)

plt.title('Distribution of Student Performance Grades\nBased on SAT Score Ranges', 
          fontsize=16, fontweight='bold', pad=20)

# Add a text box with grade definitions
grade_info = "Grade Definitions:\n• Excellent: 1400+ (Top tier)\n• Good: 1300-1399 (Above average)\n• Average: 1200-1299 (Typical range)\n• Below Average: <1200 (Needs improvement)"
plt.text(1.3, 0.5, grade_info, fontsize=11, 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8),
         verticalalignment='center')

plt.axis('equal')
plt.tight_layout()
plt.savefig(f"grades_pie_chart_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 7. STUDENT PROGRESSION SCATTER PLOT (Student Index vs Score)
plt.figure(figsize=(14, 8))

student_indices = range(len(df))
scores = df['score']

# Create scatter plot
scatter = plt.scatter(student_indices, scores, c=scores, cmap='viridis', 
                     s=60, alpha=0.7, edgecolors='black', linewidth=0.5)

# Add trend line
z = np.polyfit(student_indices, scores, 1)
p = np.poly1d(z)
plt.plot(student_indices, p(student_indices), "r--", alpha=0.8, linewidth=2, 
         label=f'Trend line (slope: {z[0]:.2f})')

# Add color bar
cbar = plt.colorbar(scatter)
cbar.set_label('SAT Score', fontsize=12, fontweight='bold')

plt.xlabel('Student Index (Order in Dataset)', fontsize=14, fontweight='bold')
plt.ylabel('SAT Score', fontsize=14, fontweight='bold')
plt.title('Student Scores by Dataset Order\nScatter Plot with Trend Analysis', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Add some statistical info
correlation = np.corrcoef(student_indices, scores)[0,1]
plt.text(0.02, 0.98, f'Correlation with index: {correlation:.3f}', 
         transform=plt.gca().transAxes, fontsize=12,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8),
         verticalalignment='top')

plt.tight_layout()
plt.savefig(f"student_progression_scatter_{timestamp}.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print(f"\n🎉 Successfully created 7 different visualizations!")
print(f"All files saved with timestamp: {timestamp}")
print("\nGenerated visualizations:")
print("1. Box Plot - Shows quartiles and outliers")
print("2. Violin Plot - Shows distribution shape and density")  
print("3. Score Ranges Bar Chart - Frequency count per score range")
print("4. Cumulative Distribution Function - Shows percentiles")
print("5. Kernel Density Estimation - Smooth distribution curve")
print("6. Performance Grades Pie Chart - Distribution by grade categories")
print("7. Student Progression Scatter Plot - Scores by dataset order with trend")