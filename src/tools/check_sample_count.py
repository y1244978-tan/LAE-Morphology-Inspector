# check_sample_count.py

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/LAE.db")

df = pd.read_sql(
    """
    SELECT sample,
           COUNT(*) AS n
    FROM galaxy
    GROUP BY sample
    """,
    conn
)

print(df)

conn.close()