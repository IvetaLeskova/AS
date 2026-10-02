# Task Manager – Data Model

## Task Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| id | UUID | Unique task identifier |
| title | String(120) | Task title |
| description | Text | Optional task description |
| status | Enum | TODO or DONE |
| created_at | DateTime | Creation timestamp in UTC |
| updated_at | DateTime | Last modification timestamp in UTC |

## Task Status

- TODO – Task is not completed.
- DONE – Task is completed.

## Initial Database

The initial application uses SQLite.

Table: `tasks`

The data model is shared conceptually across all
architectural implementations.

## Future Extensions

Project 2 may extend the task model with:

- priority
- category
- deadline
