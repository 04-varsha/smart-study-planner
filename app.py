from flask import Flask, render_template, request, redirect
from planner import generate_schedule
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('database.db')

@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks WHERE completed = 0").fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    name = request.form['name']
    hours = int(request.form['hours'])
    priority = int(request.form['priority'])

    conn = get_db()
    conn.execute("INSERT INTO tasks (name, hours, priority, completed) VALUES (?, ?, ?, 0)",
                 (name, hours, priority))
    conn.commit()
    conn.close()

    return redirect('/')

# ✅ Mark task as completed
@app.route('/complete', methods=['POST'])
def complete_task():
    task_id = request.form['task_id']

    conn = get_db()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/schedule')
def schedule():
    conn = get_db()
    tasks = conn.execute("SELECT name, hours, priority FROM tasks WHERE completed = 0").fetchall()
    conn.close()

    schedule = generate_schedule(tasks)
    return render_template('index.html', schedule=schedule, tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)