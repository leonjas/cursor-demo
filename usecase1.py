import pandas as pd
import math

# usecase1.py

df = pd.read_csv("student_score.csv")
scores = df["score"].tolist()


def summary_statistics(values):
    """
    Calculate summary statistics for a list of values.

    Args:
        values (list): A list of numerical values.

    Returns:
        dict: A dictionary containing the summary statistics.
    """
    n = len(values)
    mean = sum(values) / n
    
    # Calculate median
    sorted_values = sorted(values)
    if n % 2 == 0:
        median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        median = sorted_values[n//2]
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)
    
    return {"count": n, 
            "mean": mean, 
            "median": median,
            "std_dev": std_dev,
            "min": min(values), 
            "max": max(values)
} 


print(summary_statistics(scores))