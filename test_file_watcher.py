#!/usr/bin/env python3
"""
Test script to demonstrate the file watcher functionality
This script makes changes to student_score.csv to trigger the file watcher
"""

import time
import pandas as pd

def add_test_student():
    """Add a test student to demonstrate file watching"""
    print("🧪 Adding a test student to student_score.csv...")
    
    # Read current data
    df = pd.read_csv('student_score.csv')
    
    # Add a new test student
    new_student = {'name': f'Test Student {len(df)+1}', 'score': 1450}
    df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
    
    # Save back to CSV
    df.to_csv('student_score.csv', index=False)
    print(f"✅ Added test student. CSV now has {len(df)} students.")
    print("📊 The file watcher should automatically run usecase2.py now!")

def remove_test_students():
    """Remove test students to clean up"""
    print("🧹 Cleaning up test students...")
    
    # Read current data
    df = pd.read_csv('student_score.csv')
    
    # Remove test students
    df_cleaned = df[~df['name'].str.contains('Test Student', na=False)]
    
    # Save back to CSV
    df_cleaned.to_csv('student_score.csv', index=False)
    print(f"✅ Cleaned up. CSV now has {len(df_cleaned)} students.")
    print("📊 The file watcher should automatically run usecase2.py again!")

if __name__ == "__main__":
    print("🔍 File Watcher Test Script")
    print("=" * 40)
    
    # Test 1: Add a student
    add_test_student()
    
    # Wait a bit
    print("\n⏳ Waiting 3 seconds...")
    time.sleep(3)
    
    # Test 2: Remove test students
    remove_test_students()
    
    print("\n✨ Test complete! Check above for file watcher activity.")