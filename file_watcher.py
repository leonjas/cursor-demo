#!/usr/bin/env python3
"""
File Watcher Script
Monitors student_score.csv and automatically runs usecase2.py when the file changes.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVFileHandler(FileSystemEventHandler):
    """Event handler for CSV file changes"""
    
    def __init__(self, csv_file_path, script_to_run):
        self.csv_file_path = os.path.abspath(csv_file_path)
        self.script_to_run = script_to_run
        print(f"Watching: {self.csv_file_path}")
        print(f"Will run: {self.script_to_run}")
        print("-" * 50)
        
        # Run the script once at startup
        self.run_script("Initial run")
        
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            if file_path == self.csv_file_path:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] File modified: {event.src_path}")
                self.run_script("File modification detected")
    
    def run_script(self, trigger_reason):
        """Run the target script"""
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {trigger_reason} - Running {self.script_to_run}...")
            
            # Activate virtual environment and run the script
            venv_python = os.path.join(os.getcwd(), "venv", "bin", "python")
            result = subprocess.run([venv_python, self.script_to_run], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print(f"✅ Script completed successfully!")
                if result.stdout:
                    print(f"Output: {result.stdout.strip()}")
            else:
                print(f"❌ Script failed with return code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr.strip()}")
                    
        except Exception as e:
            print(f"❌ Error running script: {e}")
        
        print("-" * 50)

def main():
    # Configuration
    csv_file = "student_score.csv"
    script_file = "usecase2.py"
    
    # Check if files exist
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found in current directory")
        sys.exit(1)
        
    if not os.path.exists(script_file):
        print(f"Error: {script_file} not found in current directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    venv_python = os.path.join(os.getcwd(), "venv", "bin", "python")
    if not os.path.exists(venv_python):
        print("Error: Virtual environment not found. Please run the setup first.")
        sys.exit(1)
    
    print("🔍 CSV File Watcher Started")
    print("=" * 50)
    
    # Set up file system watcher
    event_handler = CSVFileHandler(csv_file, script_file)
    observer = Observer()
    
    # Watch the current directory for changes to the CSV file
    observer.schedule(event_handler, path='.', recursive=False)
    
    try:
        observer.start()
        print(f"\n👁️  Monitoring {csv_file} for changes...")
        print("Press Ctrl+C to stop watching\n")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping file watcher...")
        observer.stop()
        
    observer.join()
    print("✅ File watcher stopped")

if __name__ == "__main__":
    main()