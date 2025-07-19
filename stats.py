def summary_statistics(val):
    """
    Calculate summary statistics for a list of values without using Python built-ins.
    
    Args:
        val (list): A list of numerical values.
        
    Returns:
        dict: A dictionary containing the summary statistics.
    """
    if not val:
        return {
            'count': 0,
            'mean': None,
            'min': None,
            'max': None,
            'median': None,
            'std': None
        }
    
    # Custom sort implementation (bubble sort)
    sorted_val = val.copy()
    for i in range(len(sorted_val)):
        for j in range(0, len(sorted_val) - i - 1):
            if sorted_val[j] > sorted_val[j + 1]:
                sorted_val[j], sorted_val[j + 1] = sorted_val[j + 1], sorted_val[j]
    
    # Custom length calculation
    n = 0
    for _ in sorted_val:
        n += 1
    
    # Custom median calculation
    if n % 2 == 1:
        median = sorted_val[n // 2]
    else:
        median = (sorted_val[n // 2 - 1] + sorted_val[n // 2]) / 2
    
    # Custom sum calculation
    total = 0
    for x in val:
        total += x
    
    # Calculate mean
    mean = total / n
    
    # Custom standard deviation calculation
    variance_sum = 0
    for x in val:
        variance_sum += (x - mean) ** 2
    variance = variance_sum / n
    
    # Calculate standard deviation (square root using Newton's method)
    def sqrt(x):
        if x == 0:
            return 0
        guess = x / 2
        for _ in range(20):  # 20 iterations should be enough for convergence
            guess = (guess + x / guess) / 2
        return guess
    
    std = sqrt(variance)
    
    # Custom min/max calculation
    minimum = sorted_val[0]
    maximum = sorted_val[n - 1]
    
    return {
        'count': n,
        'mean': mean,
        'min': minimum,
        'max': maximum,
        'median': median,
        'std': std
    }