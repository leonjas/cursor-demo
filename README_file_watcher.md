# Student Score CSV File Watcher

This project implements an automated file watching system that monitors `student_score.csv` and automatically runs `usecase2.py` whenever the CSV file is modified.

## 🔧 Setup

The system has been automatically configured with:

1. **Virtual Environment**: `file_watcher_env/` with all required dependencies
2. **File Watcher Script**: `file_watcher.py` - monitors the CSV file
3. **Target Script**: `usecase2.py` - generates SAT score histogram
4. **Test Script**: `test_file_watcher.py` - demonstrates the functionality

## 🚀 How It Works

1. **File Monitoring**: The `file_watcher.py` script uses Python's `watchdog` library to monitor `student_score.csv` for changes
2. **Automatic Execution**: When changes are detected, it automatically runs `usecase2.py` using the virtual environment's Python interpreter
3. **Debouncing**: Includes a 1-second debounce to prevent multiple executions from rapid successive changes
4. **Logging**: Provides timestamped logs of all file changes and script executions

## 📊 What usecase2.py Does

The `usecase2.py` script:
- Reads data from `student_score.csv`
- Creates a histogram showing SAT score distribution in 50-point increments
- Uses matplotlib to display the visualization
- Shows scores ranging from 600 to 1650

## 🎯 Current Status

✅ **File watcher is currently running in the background**

The system is actively monitoring `student_score.csv` and will automatically:
- Detect any changes to the file
- Run `usecase2.py` to regenerate the visualization
- Display success/error messages with timestamps

## 🧪 Testing the System

To test that the file watcher is working:

1. **Using the test script**:
   ```bash
   source file_watcher_env/bin/activate
   python test_file_watcher.py
   ```

2. **Manual testing**:
   - Edit `student_score.csv` in any text editor
   - Add, modify, or remove student records
   - Save the file
   - Watch for automatic execution messages

3. **Example manual change**:
   ```bash
   echo "New Student,1400" >> student_score.csv
   ```

## 📁 Files in the Project

- `student_score.csv` - The monitored data file (student names and SAT scores)
- `usecase2.py` - The script that generates SAT score histograms
- `file_watcher.py` - The main file monitoring script
- `test_file_watcher.py` - Test script to demonstrate functionality
- `file_watcher_env/` - Python virtual environment with dependencies
- `README_file_watcher.md` - This documentation

## 🛑 Stopping the File Watcher

To stop the file watcher:
1. Find the background process: `ps aux | grep file_watcher.py`
2. Kill the process: `kill <process_id>`
3. Or use Ctrl+C if running in foreground

## 🔍 Monitoring and Logs

The file watcher provides real-time feedback:
- ✅ Success messages when `usecase2.py` runs successfully
- ❌ Error messages if something goes wrong
- 📊 Timestamps for all activities
- 🔍 File change detection notifications

## 💡 Use Cases

This automated system is perfect for:
- **Data Analysis Workflows**: Automatically update visualizations when data changes
- **Development**: Instant feedback when testing data changes
- **Monitoring**: Keep visualizations in sync with live data
- **Automation**: Reduce manual steps in data processing pipelines

---

**Note**: The file watcher is designed to be lightweight and efficient, only triggering when the specific CSV file is modified.