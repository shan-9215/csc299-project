# Simple Task Manager

A command-line task management application that stores tasks in a JSON file. This project is part of CSC299 and demonstrates basic file handling and command-line argument processing in Python.

## Features

- Store tasks with titles and descriptions
- List all stored tasks
- Search tasks by keyword
- Data persistence using JSON file

## Requirements

- Python 3.x
- No additional packages required (uses only Python standard library)

## Usage

The application supports the following commands:

### Add a new task
```bash
python3 main.py add "Task Title" "Task Description"
```

### List all tasks
```bash
python3 main.py list
```

### Search tasks
```bash
python3 main.py search "keyword"
```

### Show help
```bash
python3 main.py help
```

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the script. The file is automatically created when you add your first task.

## Repository

This project is part of the public GitHub repository [csc299-project](https://github.com/shan-9215/csc299-project).

## Project Structure

```
tasks1/
├── main.py     # Main application file
├── README.md   # Documentation
└── tasks.json  # Data file (created automatically)
```