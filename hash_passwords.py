import sqlite3
import bcrypt

DB_PATH = "database.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Select all users
cur.execute("SELECT id, password FROM users")
rows = cur.fetchall()

for user_id, plain_password in rows:
    if not plain_password:
        continue
    # Skip if already hashed (bcrypt hashes start with $2b$ or $2a$)
    if plain_password.startswith("$2b$") or plain_password.startswith("$2a$"):
        continue
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user_id))
    print(f"Hashed password for user ID {user_id}")

conn.commit()
conn.close()
print("✅ All passwords hashed successfully!")
