# Student Score CSV File Watcher

This setup automatically monitors `student_score.csv` and re-runs `usecase2.py` whenever the file changes.

## What's Running

- **File Watcher**: `file_watcher.py` is currently running in the background
- **Monitored File**: `student_score.csv` 
- **Target Script**: `usecase2.py` (creates a histogram of student SAT scores)

## How It Works

1. The file watcher monitors `student_score.csv` for any modifications
2. When a change is detected, it automatically runs `usecase2.py`
3. The script generates a matplotlib histogram showing the distribution of SAT scores

## Testing the Watcher

You can test that the file watcher is working by making changes to the CSV file:

### Option 1: Run the test script
```bash
source venv/bin/activate
python test_watcher.py
```

### Option 2: Manually edit the CSV
- Edit `student_score.csv` in any text editor
- Add, modify, or remove student records
- Save the file
- The watcher will automatically detect the change and run `usecase2.py`

### Option 3: Command line modification
```bash
echo "New Student,1450" >> student_score.csv
```

## Current Status

✅ **File Watcher is ACTIVE** - Process ID: Check with `ps aux | grep file_watcher`

## File Structure

- `student_score.csv` - Contains student names and SAT scores
- `usecase2.py` - Creates histogram of score distribution  
- `file_watcher.py` - Monitors CSV file and triggers script execution
- `test_watcher.py` - Test script to demonstrate functionality
- `venv/` - Python virtual environment with required packages

## Stopping the Watcher

To stop the file watcher:
```bash
pkill -f file_watcher.py
```

## Required Packages

The virtual environment includes:
- `watchdog` - For file system monitoring
- `pandas` - For CSV data manipulation
- `matplotlib` - For creating plots

## Notes

- The watcher runs in the background continuously
- Each file change triggers exactly one execution of `usecase2.py`
- The matplotlib plot may not display in headless environments, but the script will still run successfully
- Check the console output to see when the file watcher detects changes and runs the script