import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(posts)")
columns = cursor.fetchall()

print("POSTS TABLE COLUMNS:")
for col in columns:
    print(col)

conn.close()
