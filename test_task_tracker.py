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

