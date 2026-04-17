import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hours INTEGER,
    priority INTEGER,
    completed INTEGER DEFAULT 0
)
''')

conn.close()

print("Database created successfully!")