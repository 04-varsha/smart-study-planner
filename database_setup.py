import sqlite3

conn = sqlite3.connect("database.db")

# DELETE OLD TABLE
conn.execute("DROP TABLE IF EXISTS tasks")

# CREATE NEW TABLE
conn.execute("""
CREATE TABLE tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    marks INTEGER,
    hours INTEGER,
    completed INTEGER
)
""")

conn.commit()
conn.close()

print("Database recreated successfully")