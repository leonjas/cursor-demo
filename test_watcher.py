#!/usr/bin/env python3
"""
Test script to demonstrate the file watcher functionality.
This script adds new student records to student_score.csv to trigger automatic re-execution of usecase2.py.
"""

import pandas as pd
import time
import random

def add_random_student():
    """Add a random student record to the CSV file."""
    # Load current data
    df = pd.read_csv('student_score.csv')
    
    # Generate random student data
    first_names = ['Alex', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Jamie', 'Avery', 'Quinn', 'Sage']
    last_names = ['Anderson', 'Brown', 'Clark', 'Davis', 'Evans', 'Foster', 'Garcia', 'Harris', 'Johnson', 'King']
    
    new_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    new_score = random.randint(1000, 1600)  # SAT score range
    
    # Add new row
    new_row = pd.DataFrame({'name': [new_name], 'score': [new_score]})
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to CSV
    df.to_csv('student_score.csv', index=False)
    
    print(f"✅ Added student: {new_name} with score {new_score}")
    print(f"📊 Total students now: {len(df)}")
    
def modify_existing_score():
    """Modify an existing student's score."""
    df = pd.read_csv('student_score.csv')
    
    # Pick a random student to modify
    if len(df) > 1:
        idx = random.randint(0, len(df) - 1)
        old_score = df.loc[idx, 'score']
        new_score = random.randint(1000, 1600)
        student_name = df.loc[idx, 'name']
        
        df.loc[idx, 'score'] = new_score
        df.to_csv('student_score.csv', index=False)
        
        print(f"🔄 Modified {student_name}: {old_score} → {new_score}")

def main():
    print("🎯 File Watcher Test Script")
    print("This script will make changes to student_score.csv to trigger the file watcher")
    print("Watch for automatic execution of usecase2.py!\n")
    
    while True:
        print("\nChoose an action:")
        print("1. Add a random student")
        print("2. Modify an existing student's score")
        print("3. Wait 5 seconds and add student automatically")
        print("4. Exit")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                add_random_student()
            elif choice == '2':
                modify_existing_score()
            elif choice == '3':
                print("⏱️  Waiting 5 seconds before adding student...")
                time.sleep(5)
                add_random_student()
            elif choice == '4':
                print("👋 Exiting test script")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting test script")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()