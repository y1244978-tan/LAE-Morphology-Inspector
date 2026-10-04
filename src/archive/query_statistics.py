import sqlite3
import pandas as pd

conn = sqlite3.connect("database/LAE.db")

query = """
SELECT
    sample,
    COUNT(*) AS n,
    AVG(Re) AS mean_re,
    AVG(logM) AS mean_logM,
    AVG(concentration) AS mean_c,
    AVG(asymmetry) AS mean_a
FROM galaxy
GROUP BY sample
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()