# Task Tracker

The **Task Tracker** is a simple application built with Python that helps users manage their daily tasks. It allows users to add, edit, mark as completed, and delete tasks, while keeping track of all the changes in a simple and organized way.

## Project Description

This Python-based application provides a simple solution for managing tasks. It offers the following features:
- **Task Creation**: Add tasks with a title and description.
- **Task Completion**: Mark tasks as complete or incomplete.
- **Task Deletion**: Delete tasks that are no longer needed.
- **Persistent Storage**: Task data is saved to a local file (or database, if applicable) so tasks persist even after the program is closed.

The program allows users to interact with their tasks through a terminal interface or a graphical user interface (GUI), depending on how the application is designed.

### Key Features:
- **Add Tasks**: Users can input tasks with titles and descriptions.
- **Edit Tasks**: Users can edit existing tasks if necessary.
- **Mark Tasks as Completed**: Tasks can be marked as completed by toggling a status.
- **Delete Tasks**: Users can remove completed or unnecessary tasks.
- **Task Persistence**: Task data is saved in a local file (e.g., `.txt`, `.json`, or SQLite) to persist tasks across sessions.
- **Command-Line Interface (CLI)**: The application can be run from the terminal with various commands to manage tasks.


This project is intended to provide a lightweight and easy-to-use task management system for individuals who prefer a simple solution over complex project management tools.

## Intended Audience:
- Individuals who want a simple task management system.
- Students, professionals, or anyone looking for a basic to-do list application.
- Python enthusiasts who want to see a real-world application of Python.

## Technologies Used:
- **Python**: The core programming language used to develop the application.
- **File Storage**: Task data can be saved using local files (`.txt`, `.json`, or SQLite) for persistence.
- **Tkinter** *(Optional)*: For building a simple graphical user interface (GUI).
- **argparse** or **Click** *(Optional)*: To handle command-line interactions for the CLI version.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/task_tracker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd task_tracker
    ```

3. Install any dependencies (if applicable):
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application:

1. For the command-line interface (CLI):
    ```bash
    python task_tracker.py
    ```

2. For the graphical user interface (GUI) (if implemented with Tkinter):
    ```bash
    python task_tracker_gui.py
    ```

The app will allow you to:
- Add new tasks
- Mark tasks as complete or incomplete
- Delete tasks from the list
- View all tasks in the terminal or through the GUI

## License

This project is licensed under the MIT License.

## Acknowledgements

- Inspired by simple task management tools.
- Thanks to the Python community and contributors for helpful resources.

