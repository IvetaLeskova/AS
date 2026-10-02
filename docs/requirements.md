# Task Manager – Requirements

## 1. Overview

Task Manager is a simple application for creating, managing,
and tracking tasks.

The application serves as a common foundation for two
software architecture projects:

1. Comparison of software architectures
2. Software product line with configurable features

## 2. Core Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-01 | Create task | Create a task with a title and optional description. |
| FR-02 | List tasks | Retrieve all existing tasks. |
| FR-03 | View task | Retrieve a task by its ID. |
| FR-04 | Update task | Modify a task's title or description. |
| FR-05 | Delete task | Remove an existing task. |
| FR-06 | Change status | Mark a task as TODO or DONE. |
| FR-07 | Persistence | Store tasks persistently. |
| FR-08 | Task summary | Retrieve counts of total, TODO and DONE tasks. |

## 3. Business Rules

- Task titles are required and must not be empty.
- Maximum task title length: 120 characters.
- A new task has the status TODO.
- Supported statuses: TODO and DONE.
- Each task has a unique identifier (UUID).
- Each task has creation and modification timestamps.
- Non-existing tasks cannot be updated or deleted.

## 4. Optional Features

The following features will be used in Project 2:

| ID | Feature | Description |
|----|---------|-------------|
| FF-01 | Priorities | Assign LOW, MEDIUM or HIGH priority. |
| FF-02 | Categories | Organize tasks into categories. |
| FF-03 | Deadlines | Assign a due date to a task. |
| FF-04 | Statistics | Provide advanced task statistics. |
| FF-05 | Export | Export task reports. |

## 5. Non-Functional Requirements

- The application will expose a REST API.
- The backend will be implemented in Python.
- SQLite will be used for persistent storage.
- Automated tests will verify core functionality.
- All Project 1 implementations must provide equivalent behavior.
- Optional Project 2 features must be configurable.

## 6. Scope

The initial implementation will not include:

- User authentication
- Multiple user accounts
- Notifications
- A graphical frontend
- Cloud deployment
