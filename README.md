# Student Score File Watcher

This setup automatically monitors `student_score.csv` and re-runs `usecase2.py` (which generates a histogram of SAT scores) whenever the CSV file is modified.

## Current Status
✅ **File watcher is currently running in the background** and monitoring changes to `student_score.csv`.

## How It Works

### File Watcher (`file_watcher.py`)
- Monitors `student_score.csv` for any modifications
- Automatically runs `usecase2.py` when changes are detected
- Uses a 1-second cooldown to prevent multiple rapid executions
- Runs the script in a virtual environment with all required dependencies

### Key Features
- 🔍 **Real-time monitoring** - Detects file changes instantly
- 🚀 **Automatic execution** - No manual intervention needed
- ✅ **Error handling** - Shows success/failure status of each run
- ⏱️ **Cooldown protection** - Prevents spam execution from rapid changes
- 📊 **Initial run** - Executes the script once when watcher starts

## Files Created

1. **`file_watcher.py`** - Main file watching script
2. **`test_watcher.py`** - Interactive test script to demonstrate functionality
3. **`venv/`** - Virtual environment with dependencies (watchdog, pandas, matplotlib)

## Testing the File Watcher

### Option 1: Use the Test Script
```bash
# Activate virtual environment and run test script
source venv/bin/activate
python test_watcher.py
```

The test script provides several options:
- Add random students to the CSV
- Modify existing student scores
- Automated testing with delays

### Option 2: Manual Testing
Simply edit `student_score.csv` manually:
- Add new student records
- Modify existing scores
- Save the file

You should see automatic output showing:
- 📁 File change detection
- 🚀 Script execution start
- ✅ Successful completion
- Any error messages if issues occur

## Current File Watcher Status

The file watcher is running as process ID 2580 and actively monitoring for changes.

### To Check Status:
```bash
ps aux | grep file_watcher
```

### To Stop the Watcher:
Find the process and kill it:
```bash
pkill -f file_watcher.py
```

### To Restart the Watcher:
```bash
source venv/bin/activate
python file_watcher.py &
```

## Example Output

When you modify `student_score.csv`, you'll see output like:
```
📁 Detected change in student_score.csv
🚀 Running usecase2.py...
✅ usecase2.py completed successfully
--------------------------------------------------
```

## Dependencies

All dependencies are installed in the virtual environment:
- `watchdog` - File system monitoring
- `pandas` - Data manipulation for CSV files
- `matplotlib` - Plotting for the histogram

## Notes

- The file watcher has a 1-second cooldown to prevent excessive executions
- It only monitors the exact file `student_score.csv` (not other CSV files)
- The script runs in the background and will continue until manually stopped
- All output from `usecase2.py` is captured and displayed by the watcher