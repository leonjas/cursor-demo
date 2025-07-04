#!/usr/bin/env python3
"""
File Watcher for student_score.csv
Automatically re-runs usecase2.py whenever the CSV file changes
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVFileHandler(FileSystemEventHandler):
    """Handler for CSV file change events"""
    
    def __init__(self, csv_file, script_file):
        self.csv_file = Path(csv_file).resolve()
        self.script_file = Path(script_file).resolve()
        self.last_modified = 0
        print(f"🔍 Watching: {self.csv_file}")
        print(f"📊 Will run: {self.script_file}")
        print("-" * 50)
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
            
        # Check if the modified file is our target CSV
        event_path = Path(str(event.src_path)).resolve()
        if event_path == self.csv_file:
            # Avoid duplicate triggers by checking modification time
            current_time = time.time()
            if current_time - self.last_modified < 1:  # 1 second cooldown
                return
            self.last_modified = current_time
            
            print(f"🔄 File changed: {event.src_path}")
            self.run_script()
    
    def run_script(self):
        """Execute the Python script"""
        try:
            print(f"🚀 Running {self.script_file}...")
            result = subprocess.run([sys.executable, str(self.script_file)], 
                                  capture_output=True, text=True, cwd=self.script_file.parent)
            
            if result.returncode == 0:
                print("✅ Script executed successfully!")
                if result.stdout:
                    print("Output:", result.stdout)
            else:
                print("❌ Script execution failed!")
                if result.stderr:
                    print("Error:", result.stderr)
                    
        except Exception as e:
            print(f"❌ Error running script: {e}")
        
        print("-" * 50)

def main():
    """Main function to set up file watching"""
    csv_file = "student_score.csv"
    script_file = "usecase2_save.py"
    
    # Verify files exist
    if not Path(csv_file).exists():
        print(f"❌ Error: {csv_file} not found!")
        sys.exit(1)
        
    if not Path(script_file).exists():
        print(f"❌ Error: {script_file} not found!")
        sys.exit(1)
    
    # Set up file watcher
    event_handler = CSVFileHandler(csv_file, script_file)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    
    # Run the script once initially
    print("🎯 Running script initially...")
    event_handler.run_script()
    
    # Start watching
    observer.start()
    print(f"👀 Watching for changes to {csv_file}...")
    print("Press Ctrl+C to stop watching")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping file watcher...")
        observer.stop()
    
    observer.join()
    print("✅ File watcher stopped.")

if __name__ == "__main__":
    main()