import time
from datetime import datetime, timedelta
from peewee import *
from rich.progress import Progress
from rich.console import Console
import sys
import winsound  # Built-in sound library for Windows

# ====================
# DATABASE SETUP
# ====================
db = SqliteDatabase('tasks.db')


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    name = CharField(unique=True)
    duration = IntegerField()  # in seconds
    due_date = DateTimeField(null=True)
    recurring = CharField(null=True)  # 'daily', 'weekly', None
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)


class User(BaseModel):
    xp = IntegerField(default=0)
    level = IntegerField(default=1)
    last_login = DateTimeField(default=datetime.now)


db.connect()
db.create_tables([Task, User], safe=True)

# ====================
# GAMIFICATION SYSTEM
# ====================
console = Console()
current_user, _ = User.get_or_create(id=1)


def add_xp(amount):
    current_user.xp += amount
    while current_user.xp >= current_user.level * 100:
        current_user.xp -= current_user.level * 100
        current_user.level += 1
        console.print(f"\n[bold green]🎉 Level Up! You're now Level {current_user.level}[/]")
        play_sound("level_up")
    current_user.save()


def play_sound(sound_type):
    """Play a sound using winsound (Windows only)."""
    try:
        if sound_type == "complete":
            winsound.Beep(1000, 500)  # Beep for task completion
        elif sound_type == "level_up":
            winsound.Beep(1500, 1000)  # Beep for level up
    except Exception as e:
        console.print(f"[yellow]Couldn't play sound: {e}[/]")


# ====================
# INTERACTIVE MENU
# ====================
def show_menu():
    console.clear()
    console.rule("[bold blue]Gamified Task Manager[/]")
    console.print(f"\n[bold]Level {current_user.level}[/] | [green]XP: {current_user.xp}/{current_user.level * 100}[/]")

    choices = {
        '1': 'Add New Task',
        '2': 'Start Task',
        '3': 'View Active Tasks',
        '4': 'View Progress',
        '5': 'Exit'
    }

    for key, value in choices.items():
        console.print(f"[cyan]{key}[/]. {value}")

    while True:
        choice = input("\nEnter your choice: ").strip()
        if choice in choices:
            return choice
        console.print("[red]Invalid choice![/] Try again.")


# ====================
# TASK MANAGEMENT
# ====================
def add_task():
    console.clear()
    console.rule("[bold]Add New Task[/]")

    name = input("\nTask name: ").strip()
    duration = input("Duration (HH:MM:SS): ").strip()
    recurring = input("Recurring? (daily/weekly/n): ").strip().lower()

    # Convert duration to seconds
    try:
        h, m, s = map(int, duration.split(':'))
        duration_sec = h * 3600 + m * 60 + s
    except:
        console.print("[red]Invalid duration format![/]")
        return

    # Create task
    Task.create(
        name=name,
        duration=duration_sec,
        recurring=recurring if recurring in ('daily', 'weekly') else None,
        due_date=datetime.now() + timedelta(seconds=duration_sec)
    )

    console.print(f"\n[green]✓ Task '{name}' added![/]")
    time.sleep(1)


def start_task():
    tasks = Task.select().where(Task.completed == False)
    if not tasks:
        console.print("\n[yellow]No active tasks![/]")
        time.sleep(1)
        return

    console.clear()
    console.rule("[bold]Start a Task[/]")
    for idx, task in enumerate(tasks, 1):
        console.print(
            f"{idx}. {task.name} ({task.duration // 3600:02}:{(task.duration % 3600) // 60:02}:{task.duration % 60:02})")

    try:
        choice = int(input("\nSelect task to start: ")) - 1
        task = tasks[choice]
    except:
        console.print("[red]Invalid selection![/]")
        return

    # Run task timer
    console.clear()
    with Progress() as progress:
        task_progress = progress.add_task(f"[cyan]{task.name}", total=task.duration)
        start_time = time.time()

        while not progress.finished:
            elapsed = time.time() - start_time
            progress.update(task_progress, completed=elapsed)
            time.sleep(1)

    # Mark task complete
    task.completed = True
    if task.recurring:
        new_task = Task.create(
            name=task.name,
            duration=task.duration,
            recurring=task.recurring,
            due_date=datetime.now() + timedelta(seconds=task.duration)
        )
    task.save()

    # Award XP
    add_xp(task.duration // 60)  # 1 XP per minute
    play_sound("complete")

    console.print(f"\n[bold green]✓ Task '{task.name}' completed![/]")
    time.sleep(2)


# ====================
# PROGRESS DISPLAY
# ====================
def show_progress():
    console.clear()
    console.rule("[bold]Your Progress[/]")

    # XP Progress
    console.print(f"\n[bold]Level {current_user.level}[/]")
    xp_needed = current_user.level * 100
    progress = current_user.xp / xp_needed
    console.print(f"XP: {current_user.xp}/{xp_needed}")
    console.print(f"[green]{'█' * int(progress * 20)}[/][gray]{'░' * (20 - int(progress * 20))}[/]")

    # Active tasks
    active_tasks = Task.select().where(Task.completed == False)
    console.print("\n[bold]Active Tasks:[/]")
    for task in active_tasks:
        console.print(f"• {task.name} (Due: {task.due_date.strftime('%Y-%m-%d %H:%M')})")

    input("\nPress Enter to return...")


# ====================
# MAIN LOOP
# ====================
if __name__ == "__main__":
    try:
        while True:
            choice = show_menu()
            if choice == '1':
                add_task()
            elif choice == '2':
                start_task()
            elif choice == '3':
                show_progress()
            elif choice == '4':
                show_progress()
            elif choice == '5':
                console.print("\n[bold]Goodbye! Keep being productive! 🚀[/]")
                sys.exit()
    except KeyboardInterrupt:
        console.print("\n[bold]Goodbye! Keep being productive! 🚀[/]")
        sys.exit()