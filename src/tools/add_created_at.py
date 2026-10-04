import sqlite3

conn = sqlite3.connect(
    "database/LAE.db"
)

cursor = conn.cursor()

cursor.execute("""
ALTER TABLE classification
ADD COLUMN created_at TEXT
""")

conn.commit()
conn.close()

print("created_at added.")