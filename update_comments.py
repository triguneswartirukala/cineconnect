import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE comments ADD COLUMN parent_id INTEGER")

conn.commit()
conn.close()
print("parent_id column added")
