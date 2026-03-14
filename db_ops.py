import sqlite3

DATABASE = 'database/tasks.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# User operations
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_employees():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE role = ?', ('employee',))
    employees = cursor.fetchall()
    conn.close()
    return employees

def get_all_managers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE role = ?', ('manager',))
    managers = cursor.fetchall()
    conn.close()
    return managers

# Task operations
def get_all_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, u.username as assigned_username, c.username as created_username
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.id
        LEFT JOIN users c ON t.created_by = c.id
        ORDER BY t.created_at DESC
    ''')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_by_employee(employee_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, u.username as assigned_username, c.username as created_username
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.id
        LEFT JOIN users c ON t.created_by = c.id
        WHERE t.assigned_to = ?
        ORDER BY t.created_at DESC
    ''', (employee_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_by_status(status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, u.username as assigned_username, c.username as created_username
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.id
        LEFT JOIN users c ON t.created_by = c.id
        WHERE t.status = ?
        ORDER BY t.created_at DESC
    ''', (status,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, u.username as assigned_username, c.username as created_username
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.id
        LEFT JOIN users c ON t.created_by = c.id
        WHERE t.id = ?
    ''', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def create_task(title, description, assigned_to, created_by):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, assigned_to, created_by)
        VALUES (?, ?, ?, ?)
    ''', (title, description, assigned_to, created_by))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task_status(task_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()

def update_task(task_id, title, description, assigned_to):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET title = ?, description = ?, assigned_to = ?
        WHERE id = ?
    ''', (title, description, assigned_to, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# User management operations
def create_user(username, password, role):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', (username, password, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id')
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
