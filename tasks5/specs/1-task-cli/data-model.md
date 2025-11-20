# Data Model: Task CLI

## Entity: Task

- **Name**: Task
- **Storage**: JSON object in an array stored in the tasks file
- **Fields**:
  - `id`: integer, unique, monotonic (assigned by system)
  - `description`: string, non-empty
  - `completed`: boolean, default `false`

## Validation Rules

- `description` MUST be non-empty and trimmed of surrounding whitespace.
- `id` MUST be an integer > 0.
- `completed` MUST be a boolean.

## File format (example)

```json
[
  { "id": 1, "description": "Buy milk", "completed": false },
  { "id": 2, "description": "Pay bills", "completed": true }
]
```

## State transitions

- `add` creates a new `Task` with `completed=false`.
- `done` sets `completed=true` for the identified Task.
