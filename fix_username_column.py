import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 1. Add username column
try:
    cursor.execute("""
    ALTER TABLE users
    ADD COLUMN username TEXT
    """)
    print("Username column added")
except sqlite3.OperationalError:
    print("Username column already exists")

# 2. Backfill username for existing users
cursor.execute("SELECT id, email FROM users WHERE username IS NULL")
users = cursor.fetchall()

for user in users:
    user_id, email = user
    username = email.split("@")[0].lower()
    cursor.execute(
        "UPDATE users SET username=? WHERE id=?",
        (username, user_id)
    )

conn.commit()
conn.close()

print("Existing users updated with usernames")
