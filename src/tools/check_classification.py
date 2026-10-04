import sqlite3
import pandas as pd

conn = sqlite3.connect("database/LAE.db")

df = pd.read_sql(
    "SELECT * FROM classification",
    conn
)

print(df)

conn.close()
