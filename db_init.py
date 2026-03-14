import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect('database/tasks.db')
    cursor = conn.cursor()
    
    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    employee_password = bcrypt.hashpw('emp123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('manager', 'employee'))
        )
    ''')
    
    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'not_started' CHECK(status IN ('not_started', 'ongoing', 'done')),
            assigned_to INTEGER,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Insert default users
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES ('admin', ?, 'manager')
    ''', (admin_password,))
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES ('employee1', ?, 'employee')
    ''', (employee_password,))
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES ('employee2', ?, 'employee')
    ''', (employee_password,))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
