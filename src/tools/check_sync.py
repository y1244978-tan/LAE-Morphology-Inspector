import sqlite3
import pandas as pd

csv_df = pd.read_csv(
    "output/results_master.csv"
)

conn = sqlite3.connect(
    "database/LAE.db"
)

db_df = pd.read_sql(
    "SELECT * FROM classification",
    conn
)

conn.close()

print("CSV件数 :", len(csv_df))
print("DB件数  :", len(db_df))