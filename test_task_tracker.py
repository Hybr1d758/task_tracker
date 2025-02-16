# filepath: /Users/edwardjr/Documents/Data Science/Data Analysis/task_tracker/tests/test_task_tracker.py
import pytest
from task_tracker import add_task, update_task, delete_task, list_tasks, search_tasks, undo_last_action, export_to_csv, load_tasks, init_db

@pytest.fixture(autouse=True)
def setup_db():
    # Initialize the database before each test
    init_db()

def test_add_task():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0][1] == "Test Task"
    assert tasks[0][2] == "todo"
    assert tasks[0][3] == "2025-02-20"
    assert tasks[0][4] == "high"
    assert tasks[0][5] == "weekly"

def test_update_task():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    tasks = load_tasks()
    task_id = tasks[0][0]
    update_task(task_id, "Updated Task")
    tasks = load_tasks()
    assert tasks[0][1] == "Updated Task"

def test_delete_task():
    add_task("Test Task", "2025-02-20", "high", "weekly")
    tasks = load_tasks()
    task_id = tasks[0][0]
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
    assert results[0][1] == "Test Task 1"

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