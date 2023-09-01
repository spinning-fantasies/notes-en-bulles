import sqlite3

# Setup SQLite database
conn = sqlite3.connect('thoughts.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS thoughts (
        id INTEGER PRIMARY KEY,
        created_at TEXT,
        title TEXT,
        content TEXT,
        groups_id INTEGER,
        categories TEXT,
        is_deleted INTEGER DEFAULT 0
    );
''')

conn.commit()
conn.close()