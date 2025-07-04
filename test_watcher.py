#!/usr/bin/env python3
"""
Test script to demonstrate the file watcher functionality
"""

import time
import pandas as pd

def modify_csv_file():
    """Make a simple modification to the CSV file to trigger the watcher"""
    
    # Read the current CSV
    df = pd.read_csv('student_score.csv')
    print(f"Current CSV has {len(df)} rows")
    
    # Add a new test student
    timestamp = int(time.time())
    new_student = pd.DataFrame({
        'name': [f'Test Student {timestamp}'],
        'score': [1500 + (timestamp % 100)]
    })
    
    # Append to existing data
    df_updated = pd.concat([df, new_student], ignore_index=True)
    
    # Save back to file (this will trigger the file watcher)
    df_updated.to_csv('student_score.csv', index=False)
    print(f"Added test student. CSV now has {len(df_updated)} rows")
    print("This should trigger the file watcher to re-run usecase2.py!")

if __name__ == "__main__":
    modify_csv_file()