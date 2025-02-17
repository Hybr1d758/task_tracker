import pytest
import os
from task_tracker import add_task, update_task, delete_task, list_tasks, search_tasks, undo_last_action, export_to_csv, load_tasks

@pytest.fixture(autouse=True)
def setup_tasks():
    # Initialize the tasks before each test
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")

def test_add_task():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"
    assert tasks[0]["status"] == "todo"
    assert tasks[0]["due_date"] == "2025-02-20"
    assert tasks[0]["priority"] == "high"
    assert tasks[0]["repeat"] == "weekly"

def test_update_task():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    tasks = load_tasks()
    task_id = tasks[0]["id"]
    update_task(task_id, "Updated Task")
    tasks = load_tasks()
    assert tasks[0]["title"] == "Updated Task"

def test_delete_task():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    tasks = load_tasks()
    task_id = tasks[0]["id"]
    delete_task(task_id)
    tasks = load_tasks()
    assert len(tasks) == 0

def test_list_tasks():
    add_task("Test Task 1", "2025-02-20", "high", "weekly")
    add_task("Test Task 2", "2025-02-21", "medium", "daily")
    tasks = load_tasks()
    assert len(tasks) == 2

def test_search_tasks():
    add_task("Test Task 1", "2025-02-20", "high", "weekly")
    add_task("Another Task", "2025-02-21", "medium", "daily")
    results = search_tasks("Test")
    assert len(results) == 1
    assert results[0]["title"] == "Test Task 1"

def test_undo_last_action():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    delete_task(1)
    undo_last_action()
    tasks = load_tasks()
    assert len(tasks) == 1

def test_export_to_csv():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    export_to_csv()
    with open("tasks.csv", "r") as file:
        lines = file.readlines()
        assert len(lines) == 2  # Header + 1 task

import json
import argparse
import os
import shutil
import csv
from datetime import datetime

# Define the file where tasks will be stored
TASKS_FILE = "tasks.json"

# Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []  # Return an empty list if the file does not exist
    with open(TASKS_FILE, "r") as file:
        return json.load(file)  # Load and return the tasks from the file

# Save tasks to the JSON file
def save_tasks(tasks):
    if os.path.exists(TASKS_FILE):
        shutil.copy(TASKS_FILE, TASKS_FILE + ".bak")  # Create a backup before saving
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)  # Save the tasks to the file with indentation

# Add a new task to the list
def add_task(title, due_date=None, priority="medium", repeat=None):
    tasks = load_tasks()  # Load existing tasks
    task = {
        "id": len(tasks) + 1,  # Assign a new ID to the task
        "title": title,
        "status": "todo",
        "due_date": due_date,
        "priority": priority,
        "repeat": repeat
    }
    tasks.append(task)  # Add the new task to the list
    save_tasks(tasks)  # Save the updated list of tasks
    print(f"Task added: {title} (Priority: {priority}, Due: {due_date}, Repeats: {repeat})")

# Update the title of an existing task
def update_task(task_id, title):
    tasks = load_tasks()  # Load existing tasks
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title  # Update the task title
            save_tasks(tasks)  # Save the updated list of tasks
            print("Task updated.")
            return
    print("Task not found.")  # Print a message if the task was not found

# Delete a task from the list
def delete_task(task_id):
    tasks = load_tasks()  # Load existing tasks
    tasks = [task for task in tasks if task["id"] != task_id]  # Remove the task with the given ID
    save_tasks(tasks)  # Save the updated list of tasks
    print("Task deleted.")

# List all tasks, optionally sorted by a specified field
def list_tasks(sort_by=None):
    tasks = load_tasks()  # Load existing tasks
    if sort_by:
        tasks = sorted(tasks, key=lambda x: x.get(sort_by))  # Sort tasks by the specified field
    for task in tasks:
        print(task)  # Print each task

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            if status == "done":
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print("Task not found.")

def search_tasks(keyword):
    tasks = load_tasks()
    results = []
    for task in tasks:
        task_title = task["title"].lower()
        if keyword.lower() in task_title:
            results.append(task)
    return results

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