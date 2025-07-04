#!/usr/bin/env python3
"""
File Watcher for student_score.csv
Automatically runs usecase2.py whenever student_score.csv is modified.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVFileHandler(FileSystemEventHandler):
    """Handler for CSV file changes"""
    
    def __init__(self, csv_file, script_to_run, python_path):
        self.csv_file = csv_file
        self.script_to_run = script_to_run
        self.python_path = python_path
        self.last_run_time = 0
        self.debounce_time = 1  # Wait 1 second between runs to avoid multiple triggers
        
    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return
            
        # Check if the modified file is our target CSV file
        if os.path.basename(event.src_path) == self.csv_file:
            current_time = time.time()
            
            # Debounce: only run if enough time has passed since last run
            if current_time - self.last_run_time >= self.debounce_time:
                self.last_run_time = current_time
                self.run_script()
    
    def run_script(self):
        """Execute the target script"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] Detected change in {self.csv_file}")
        print(f"[{timestamp}] Running {self.script_to_run}...")
        
        try:
            # Run the script using the virtual environment's Python
            result = subprocess.run(
                [self.python_path, self.script_to_run],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                print(f"[{timestamp}] ✅ {self.script_to_run} executed successfully!")
                if result.stdout:
                    print(f"Output: {result.stdout}")
            else:
                print(f"[{timestamp}] ❌ Error running {self.script_to_run}")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"[{timestamp}] ❌ Exception occurred: {str(e)}")

def main():
    # Configuration
    csv_file = "student_score.csv"
    script_to_run = "usecase2.py"
    python_path = "./file_watcher_env/bin/python"
    watch_directory = "."
    
    # Check if files exist
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found in current directory")
        sys.exit(1)
        
    if not os.path.exists(script_to_run):
        print(f"❌ Error: {script_to_run} not found in current directory")
        sys.exit(1)
        
    if not os.path.exists(python_path):
        print(f"❌ Error: Python virtual environment not found at {python_path}")
        sys.exit(1)
    
    # Create event handler and observer
    event_handler = CSVFileHandler(csv_file, script_to_run, python_path)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=False)
    
    # Start watching
    observer.start()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔍 [{start_time}] File watcher started!")
    print(f"📁 Watching: {os.path.abspath(csv_file)}")
    print(f"🚀 Will run: {script_to_run}")
    print(f"🐍 Using Python: {os.path.abspath(python_path)}")
    print(f"📍 Working directory: {os.getcwd()}")
    print("\n📝 Waiting for changes to student_score.csv...")
    print("   (Press Ctrl+C to stop)")
    
    # Run the script once initially
    print(f"\n🎯 Running {script_to_run} initially...")
    event_handler.run_script()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        stop_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🛑 [{stop_time}] File watcher stopped.")
    
    observer.join()

if __name__ == "__main__":
    main()