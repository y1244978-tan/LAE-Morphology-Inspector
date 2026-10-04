import sqlite3

conn = sqlite3.connect("database/LAE.db")
cur = conn.cursor()

cur.execute("""
DELETE FROM classification
""")

conn.commit()

print("classification table cleared")

conn.close()