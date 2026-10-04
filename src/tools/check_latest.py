import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/LAE.db"
)

df = pd.read_sql(
    """
    SELECT
        id,
        memo,
        created_at
    FROM classification
    ORDER BY created_at DESC
    LIMIT 20
    """,
    conn
)

print(df)

conn.close()