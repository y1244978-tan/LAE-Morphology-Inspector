from database import get_ranked_galaxies




import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/LAE.db"
)

df = pd.read_sql(
    """
    SELECT *
    FROM classification
    WHERE detectable = 0
      AND bright_neighbor = 0
      AND multiple_component = 0
      AND point_source = 0
    """,
    conn
)

print(df)

print(
    "\n0,0,0,0の天体数:",
    len(df)
)

conn.close()