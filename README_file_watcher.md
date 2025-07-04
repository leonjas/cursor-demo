# Student Score CSV File Watcher

This file watcher automatically monitors `student_score.csv` and re-runs the analysis script whenever the CSV file is modified.

## Files

- **`file_watcher.py`** - Watches `student_score.csv` and runs `usecase2_save.py` (saves histogram images with timestamps)
- **`file_watcher_original.py`** - Watches `student_score.csv` and runs `usecase2.py` (displays histogram with plt.show())
- **`usecase2_save.py`** - Modified version that saves histogram images with timestamps
- **`usecase2.py`** - Original script that displays histogram

## How to Use

### Option 1: Save Histogram Images (Recommended for monitoring)
```bash
python file_watcher.py
```
This will:
- Monitor `student_score.csv` for changes
- Run `usecase2_save.py` whenever the file changes
- Generate timestamped PNG files showing the histogram
- Display output messages showing when files change and scripts run

### Option 2: Display Histogram (Original behavior)
```bash
python file_watcher_original.py
```
This will:
- Monitor `student_score.csv` for changes  
- Run `usecase2.py` whenever the file changes
- Display the histogram using `plt.show()` (requires display capability)

## Features

- **Real-time monitoring** - Detects file changes immediately
- **Duplicate prevention** - Prevents multiple triggers for rapid successive changes
- **Error handling** - Shows clear error messages if scripts fail
- **Initial run** - Executes the script once when starting the watcher
- **Clean shutdown** - Press `Ctrl+C` to stop watching gracefully

## Requirements

- Python 3.x
- `watchdog` library (`pip install watchdog`)
- `pandas` and `matplotlib` (for the analysis scripts)

## Testing

To test the file watcher:
1. Start the watcher with `python file_watcher.py`
2. Edit `student_score.csv` (add/modify student records)
3. Save the file
4. Watch for new timestamped histogram PNG files to be generated

## Example Output

```
🔍 Watching: /workspace/student_score.csv
📊 Will run: /workspace/usecase2_save.py
--------------------------------------------------
🎯 Running script initially...
🚀 Running /workspace/usecase2_save.py...
✅ Script executed successfully!
Output: Histogram saved as: student_score_histogram_20250704_043837.png
Total students: 102
Score range: 1100 - 1520
--------------------------------------------------
👀 Watching for changes to student_score.csv...
Press Ctrl+C to stop watching
🔄 File changed: /workspace/student_score.csv
🚀 Running /workspace/usecase2_save.py...
✅ Script executed successfully!
Output: Histogram saved as: student_score_histogram_20250704_043846.png
Total students: 103
Score range: 1100 - 1600
--------------------------------------------------