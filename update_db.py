import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN skills TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN location TEXT")

conn.commit()
conn.close()

print("Profile fields added successfully")
