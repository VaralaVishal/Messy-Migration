import sqlite3
import bcrypt

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Hash the sample passwords
password1 = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
password2 = bcrypt.hashpw('secret456'.encode('utf-8'), bcrypt.gensalt())
password3 = bcrypt.hashpw('qwerty789'.encode('utf-8'), bcrypt.gensalt())

cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", ('John Doe', 'john@example.com', password1))
cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", ('Jane Smith', 'jane@example.com', password2))
cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", ('Bob Johnson', 'bob@example.com', password3))

conn.commit()
conn.close()
print("Database initialized with sample data (hashed passwords)")
