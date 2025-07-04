import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVFileHandler(FileSystemEventHandler):
    def __init__(self, csv_file, script_file):
        self.csv_file = csv_file
        self.script_file = script_file
        self.last_run_time = 0
        print(f"🔍 Watching for changes to {csv_file}")
        print(f"📊 Will run {script_file} automatically when changes detected")
        print("Press Ctrl+C to stop watching\n")
        
        # Run the script once at startup
        self.run_script()
    
    def on_modified(self, event):
        # Check if the modified file is our target CSV file
        if event.is_directory:
            return
            
        # Get the absolute path of the modified file
        modified_file = os.path.abspath(event.src_path)
        target_file = os.path.abspath(self.csv_file)
        
        if modified_file == target_file:
            # Add a small delay to avoid multiple rapid executions
            current_time = time.time()
            if current_time - self.last_run_time > 1:  # 1 second cooldown
                print(f"📁 Detected change in {self.csv_file}")
                self.run_script()
                self.last_run_time = current_time
    
    def run_script(self):
        try:
            print(f"🚀 Running {self.script_file}...")
            # Use the virtual environment's Python interpreter
            result = subprocess.run([
                './venv/bin/python', self.script_file
            ], capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                print(f"✅ {self.script_file} completed successfully")
                if result.stdout:
                    print("Output:", result.stdout)
            else:
                print(f"❌ Error running {self.script_file}")
                if result.stderr:
                    print("Error:", result.stderr)
        except Exception as e:
            print(f"❌ Failed to run {self.script_file}: {e}")
        print("-" * 50)

def main():
    csv_file = "student_score.csv"
    script_file = "usecase2.py"
    
    # Check if files exist
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        return
    
    if not os.path.exists(script_file):
        print(f"❌ Error: {script_file} not found!")
        return
    
    # Set up file watcher
    event_handler = CSVFileHandler(csv_file, script_file)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    
    # Start watching
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping file watcher...")
        observer.stop()
    
    observer.join()
    print("👋 File watcher stopped.")

if __name__ == "__main__":
    main()