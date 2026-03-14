# Employee Task Management

Employee Task Management is a small Flask web application for assigning work, tracking task status, and managing users with `manager` and `employee` roles. It uses server-rendered HTML templates and a local SQLite database.

## Features

- Authenticates users with role-based sessions
- Lets managers create, edit, assign, and delete tasks
- Lets employees view only their assigned tasks
- Lets employees update task status to `not_started`, `ongoing`, or `done`
- Lets managers add and delete users
- Stores application data in SQLite

## Tech Stack

- Python 3
- Flask
- SQLite
- Jinja2 templates
- CSS

## Project Structure

- `app.py` - Flask application and route handlers
- `db_ops.py` - database query and mutation helpers
- `db_init.py` - database schema creation and seed data
- `database/tasks.db` - SQLite database file
- `templates/` - HTML templates for login, dashboard, task forms, and user management
- `static/` - CSS styles for a better UI/UX

## Getting Started

### Prerequisites

- Python 3.10 or newer

### Installation

1. Create a virtual environment.
2. Activate it.
3. Install Flask.

```bash
pip install flask
```

### Initialize the Database

Run the initializer once before starting the app:

```bash
python db_init.py
```

This creates the `users` and `tasks` tables and seeds a default manager and two employees.

### Start the Application

```bash
python app.py
```

The development server starts at `http://127.0.0.1:5000`.

## Default Login Credentials

Use the seeded accounts after running `db_init.py`:

| Role | Username | Password |
| --- | --- | --- |
| Manager | `admin` | `admin123` |
| Employee | `employee1` | `emp123` |
| Employee | `employee2` | `emp123` |

## User Roles

### Manager

- View every task in the system
- Create new tasks
- Edit task title, description, and assignee
- Delete tasks
- View all users
- Add or delete users

### Employee

- View only tasks assigned to their account
- Update the status of their own tasks

## Main Routes

| Route | Methods | Purpose |
| --- | --- | --- |
| `/` | `GET` | Redirects to login or dashboard |
| `/login` | `GET`, `POST` | User login |
| `/logout` | `GET` | Clear session and sign out |
| `/dashboard` | `GET` | Role-based task dashboard |
| `/task/create` | `GET`, `POST` | Manager-only task creation |
| `/task/<task_id>/edit` | `GET`, `POST` | Manager-only task editing |
| `/task/<task_id>/delete` | `POST` | Manager-only task deletion |
| `/task/<task_id>/update_status` | `POST` | Task status update |
| `/tasks` | `GET` | Manager-only task listing |
| `/users` | `GET` | Manager-only user listing |
| `/user/add` | `GET`, `POST` | Manager-only user creation |
| `/user/<user_id>/delete` | `POST` | Manager-only user deletion |

## Database Schema

### `users`

- `id` - integer primary key
- `username` - unique text value
- `password` - plain text password
- `role` - `manager` or `employee`

### `tasks`

- `id` - integer primary key
- `title` - required task title
- `description` - optional task details
- `status` - `not_started`, `ongoing`, or `done`
- `assigned_to` - optional foreign key to `users.id`
- `created_by` - foreign key to `users.id`
- `created_at` - timestamp with default current time

## Notes and Current Limitations

- Passwords are stored in plain text and should be hashed before production use.
- The Flask `secret_key` is hardcoded in `app.py`.
- The application runs with `debug=True`.
- There is no automated test suite in the current project.
- This project is a web app, not a JSON REST API.
## Development Notes

- Database path: `database/tasks.db`
- To reset local data, delete `database/tasks.db` and run `python db_init.py` again.
- Some CSS styling and README.md was initially generated with the assistance of AI coding tools and then adjusted manually during development.

