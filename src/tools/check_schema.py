import sqlite3

conn = sqlite3.connect(
    "database/LAE.db"
)

cursor = conn.cursor()

cursor.execute("""
PRAGMA table_info(classification)
""")

for row in cursor.fetchall():
    print(row)

conn.close()