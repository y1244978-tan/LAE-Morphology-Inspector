import sqlite3

conn = sqlite3.connect(
    "database/LAE.db"
)

cursor = conn.cursor()

cursor.execute(
    "DELETE FROM galaxy"
)

conn.commit()
conn.close()

print("galaxy table cleared.")