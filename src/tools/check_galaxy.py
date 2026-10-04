import sqlite3
import pandas as pd

conn = sqlite3.connect("database/LAE.db")

df = pd.read_sql(
    "SELECT * FROM galaxy",
    conn
)

print(df.head())
print()
print("登録件数:", len(df))

conn.close()