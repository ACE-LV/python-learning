# 7 Day Project Plan - User Data Manager

## Goal

In 7 days, complete a usable Python mini project with:

- SQLite database integration
- CLI commands for CRUD-like operations
- JSON import/export
- basic tests and refactor

## Day 1 - Understand and run existing project

Tasks:

1. Run `init-db`, `seed`, `list`, `report` successfully.
2. Read `src/main.py` and explain each function in your own words.
3. Add one new command: `get --user-id`.

Done criteria:

- Can run all existing commands with no errors.
- `get --user-id` returns one user or `User not found`.

## Day 2 - Input validation and errors

Tasks:

1. Add validation for `add` command:
   - `name` cannot be empty.
   - `role` must be one of `frontend/backend/qa`.
2. Add friendly error messages for invalid input.
3. Keep unknown exceptions visible (do not silently swallow).

Done criteria:

- Invalid input is rejected with clear message.
- Valid input still works.

## Day 3 - Query filters

Tasks:

1. Extend `list` command:
   - `--active true|false`
   - `--role frontend|backend|qa`
2. Keep SQL parameterized (no string-concatenated SQL).

Done criteria:

- `list` can filter by active/role independently and together.

## Day 4 - Update and delete

Tasks:

1. Add command: `update-role --user-id --role`.
2. Add command: `delete --user-id`.
3. Return clear result messages: success/not found.

Done criteria:

- Role update and delete both work.
- Not-found cases are handled.

## Day 5 - Export and report enhancement

Tasks:

1. Add command: `export-json --output path`.
2. Enhance `report`:
   - include inactive count
   - include names grouped by role

Done criteria:

- Can export all users to a JSON file.
- Report is richer and still readable.

## Day 6 - Refactor structure

Tasks:

1. Split `main.py` into modules:
   - `models.py`
   - `repository.py`
   - `services.py`
   - `cli.py`
2. Keep behavior unchanged.

Done criteria:

- All commands still run after split.
- Code is easier to read.

## Day 7 - Testing and wrap-up

Tasks:

1. Add basic tests for repository methods:
   - add user
   - deactivate user
   - count by role
2. Add one CLI smoke test flow (init -> seed -> list).
3. Write project summary (what learned, next improvements).

Done criteria:

- Core tests pass.
- You can explain project architecture and next steps.

## Daily habit (20-30 min)

1. Run one command manually.
2. Make one small change.
3. Verify change.
4. Write 3-line summary.

## Suggested command set

```powershell
Set-Location "c:\Users\ace.lv\workspace\project\python-learning"
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py init-db
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py seed
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py list
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py report
```
