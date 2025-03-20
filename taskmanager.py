import sqlite3
import typer
from rich.console import Console
from rich.table import Table

# Initialize CLI app and console
app = typer.Typer()
console = Console()

# Database setup
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),
            status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO user_progress (id, xp, level, streak) VALUES (1, 0, 1, 0)")
    conn.commit()
    conn.close()

# Add task
@app.command()
def add_task(name: str, priority: str = "Medium"):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, priority) VALUES (?, ?)", (name, priority))
    conn.commit()
    conn.close()
    console.print(f"[green]Task '{name}' added with priority {priority}.[/green]")

# Show tasks
@app.command()
def show_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    table = Table(title="Task List")
    table.add_column("ID", justify="center")
    table.add_column("Task Name", justify="left")
    table.add_column("Priority", justify="center")
    table.add_column("Status", justify="center")
    for task in tasks:
        table.add_row(str(task[0]), task[1], task[2], task[3])
    console.print(table)

# Complete task & Earn XP
@app.command()
def complete_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT priority FROM tasks WHERE id = ? AND status = 'Pending'", (task_id,))
    task = cursor.fetchone()
    if not task:
        console.print("[red]Task not found or already completed![/red]")
        return
    priority = task[0]
    xp_earned = {"Low": 5, "Medium": 10, "High": 20}.get(priority, 5)
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    cursor.execute("UPDATE user_progress SET xp = xp + ? WHERE id = 1", (xp_earned,))
    conn.commit()
    conn.close()
    console.print(f"[blue]Task {task_id} completed! You earned {xp_earned} XP.[/blue]")
    check_level_up()

# Check XP & Level
@app.command()
def show_progress():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT xp, level FROM user_progress WHERE id = 1")
    xp, level = cursor.fetchone()
    conn.close()
    console.print(f"[yellow]XP: {xp} | Level: {level}[/yellow]")

# Level-up logic
def check_level_up():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT xp, level FROM user_progress WHERE id = 1")
    xp, level = cursor.fetchone()
    new_level = (xp // 100) + 1
    if new_level > level:
        console.print(f"[green]Congratulations! You leveled up to Level {new_level}![/green]")
        cursor.execute("UPDATE user_progress SET level = ? WHERE id = 1", (new_level,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app()