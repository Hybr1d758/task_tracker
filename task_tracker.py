import json
import argparse
import os
import shutil
import csv
from datetime import datetime
import sqlite3

# Define the file where tasks will be stored
TASKS_FILE = "tasks.json"

# Gmail credentials (replace with your actual credentials)
GMAIL_USER = 'your_email@gmail.com'
GMAIL_PASSWORD = 'your_password'

# Your phone number (replace with your actual phone number)
YOUR_PHONE_NUMBER = '1234567890'

# Load tasks from the database
def load_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Save a task to the database
def save_task(task):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, status, due_date, priority, repeat, note)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task['title'], task['status'], task['due_date'], task['priority'], task['repeat'], task.get('note')))
    conn.commit()
    conn.close()

# Add a new task to the list
def add_task(title, due_date=None, priority="medium", repeat=None):
    task = {
        "title": title,
        "status": "todo",
        "due_date": due_date,
        "priority": priority,
        "repeat": repeat
    }
    save_task(task)  # Save the new task to the database
    print(f"Task added: {title} (Priority: {priority}, Due: {due_date}, Repeats: {repeat})")

# Update the title of an existing task
def update_task(task_id, title):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
    conn.commit()
    conn.close()
    print("Task updated.")

# Delete a task from the list
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted.")

# List all tasks, optionally sorted by a specified field
def list_tasks(sort_by=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    if sort_by:
        cursor.execute(f'SELECT * FROM tasks ORDER BY {sort_by}')
    else:
        cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        print(task)

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            if status == "done":
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET status = ?, completed_at = ?
                WHERE id = ?
            ''', (status, task.get("completed_at"), task_id))
            conn.commit()
            conn.close()
            print(f"Task {task_id} marked as {status}.")
            return
    print("Task not found.")

def search_tasks(keyword):
    tasks = load_tasks()
    results = [task for task in tasks if keyword.lower() in task["title"].lower()]
    if results:
        for task in results:
            print(f"[{task['id']}] {task['title']} - {task['status']}")
    else:
        print("No tasks found.")

def undo_last_action():
    if os.path.exists(TASKS_FILE + ".bak"):
        shutil.copy(TASKS_FILE + ".bak", TASKS_FILE)
        print("Undo successful!")
    else:
        print("No previous action to undo.")

def export_to_csv():
    tasks = load_tasks()
    with open("tasks.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Title", "Status", "Due Date", "Priority", "Repeats"])
        for task in tasks:
            writer.writerow([task["id"], task["title"], task["status"], task.get("due_date", ""), task.get("priority", ""), task.get("repeat", "")])
    print("Tasks exported to tasks.csv")

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            priority TEXT,
            repeat TEXT,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument("command", choices=["add", "update", "delete", "list", "done", "todo", "progress", "search", "undo", "export"], help="Command to execute")
    parser.add_argument("--id", type=int, help="Task ID")
    parser.add_argument("--title", type=str, help="Task title")
    parser.add_argument("--due", type=str, help="Due date (YYYY-MM-DD)")
    parser.add_argument("--priority", type=str, choices=["low", "medium", "high"], help="Task priority")
    parser.add_argument("--repeat", type=str, choices=["daily", "weekly", "monthly"], help="Recurring task frequency")
    parser.add_argument("--keyword", type=str, help="Keyword to search for")
    parser.add_argument("--sort", type=str, choices=["priority", "due_date"], help="Sort tasks by priority or due date")
    
    args = parser.parse_args()
    
    init_db()  # Initialize the database

    if args.command == "add" and args.title:
        add_task(args.title, args.due, args.priority, args.repeat)
    elif args.command == "update" and args.id and args.title:
        update_task(args.id, args.title)
    elif args.command == "delete" and args.id:
        delete_task(args.id)
    elif args.command == "list":
        list_tasks(args.sort)
    elif args.command == "done" and args.id:
        mark_task(args.id, "done")
    elif args.command == "todo" and args.id:
        mark_task(args.id, "todo")
    elif args.command == "progress" and args.id:
        mark_task(args.id, "in progress")
    elif args.command == "search" and args.keyword:
        search_tasks(args.keyword)
    elif args.command == "undo":
        undo_last_action()
    elif args.command == "export":
        export_to_csv()
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()
