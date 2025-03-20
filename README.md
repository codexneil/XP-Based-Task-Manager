# XP-Based-Task-Manager
 The project incorporates gamification elements like XP points, levels, and achievements to motivate users. Built using Python 3.13.1, it leverages the peewee library for database management and rich for rich terminal formatting. Sound alerts are implemented using winsound for Windows. 

A command-line task manager with gamification features (XP, levels, progress bars) to make productivity fun! Built with Python.

Prerequisites
Python 3.13.1 or later (Download Python)

Git (optional, for cloning the repository)

Windows OS (for sound alerts; macOS/Linux users can skip sound features).


Installation
1. Clone the Repository:
   ```cmd
   git clone https://github.com/yourusername/gamified-task-manager.git
   cd gamified-task-manager

2. Set Up a Virtual Environment (recommended):
   ```cmd
   python -m venv venv
3. Activate the environment:
   ```cmd
   .\venv\Scripts\activate
4. Install Dependencies:
   ```cmd
   pip install peewee rich

5. Running the Project
   ```cmd
   python task_manager.py


Usage
1. Main Menu:
   Choose options using number keys (1 to 5).
   Example: Press 1 to add a task, 2 to start a task timer.

2. Add a Task:
   Enter task name, duration (HH:MM:SS), and recurrence (daily/weekly).

3. Start a Task:
   Select a task from the list to start its timer. A progress bar will show live updates.

4. View Progress:
   Check your XP, level, and active tasks.

5. Sound Alerts (Windows only):
   A beep will play on task completion and level-up.


Testing

1. Add a test task (e.g., "Write Documentation", duration 00:05:00).
2. Start the task and let the timer run. You’ll earn XP and level up after completion.


Troubleshooting

1. ModuleNotFoundError: Ensure dependencies are installed (pip install peewee rich).
2. Sound Issues: On non-Windows systems, comment out winsound code in task_manager.py.
3. Database Issues: Delete tasks.db to reset progress.
