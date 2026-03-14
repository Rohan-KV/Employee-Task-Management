from flask import *
import db_ops

app = Flask(__name__)
app.secret_key = 'task-management-secret-key'

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db_ops.get_user_by_username(username)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    role = session['role']
    
    if role == 'manager':
        tasks = db_ops.get_all_tasks()
    else:
        tasks = db_ops.get_tasks_by_employee(user_id)
    
    return render_template('dashboard.html', tasks=tasks, role=role, username=session['username'])

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        
        if title:
            assigned_to_id = int(assigned_to) if assigned_to else None
            db_ops.create_task(title, description, assigned_to_id, session['user_id'])
            return redirect(url_for('dashboard'))
    
    employees = db_ops.get_all_employees()
    return render_template('create_task.html', employees=employees)

@app.route('/task/<int:task_id>/update_status', methods=['POST'])
def update_task_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    status = request.form.get('status')
    task = db_ops.get_task_by_id(task_id)
    
    if task:
        # Employees can only update their own tasks
        if session['role'] == 'employee' and task['assigned_to'] != session['user_id']:
            return redirect(url_for('dashboard'))
        
        db_ops.update_task_status(task_id, status)
    
    return redirect(url_for('dashboard'))

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    task = db_ops.get_task_by_id(task_id)
    if not task:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        
        if title:
            assigned_to_id = int(assigned_to) if assigned_to else None
            db_ops.update_task(task_id, title, description, assigned_to_id)
            return redirect(url_for('dashboard'))
    
    employees = db_ops.get_all_employees()
    return render_template('edit_task.html', task=task, employees=employees)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    db_ops.delete_task(task_id)
    return redirect(url_for('dashboard'))

@app.route('/tasks')
def view_all_tasks():
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    tasks = db_ops.get_all_tasks()
    return render_template('all_tasks.html', tasks=tasks)

@app.route('/users')
def view_all_users():
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    users = db_ops.get_all_users()
    return render_template('all_users.html', users=users)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if username and password and role:
            user_id = db_ops.create_user(username, password, role)
            if user_id:
                return redirect(url_for('view_all_users'))
            else:
                return render_template('add_user.html', error='Username already exists')
    
    return render_template('add_user.html', error=None)

@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or session['role'] != 'manager':
        return redirect(url_for('dashboard'))
    
    db_ops.delete_user(user_id)
    return redirect(url_for('view_all_users'))

if __name__ == '__main__':
    app.run(debug=True)
