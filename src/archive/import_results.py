import sqlite3
import pandas as pd

# CSV読み込み
df = pd.read_csv("output/results.csv")

# DB接続
conn = sqlite3.connect("database/LAE.db")

# テーブルへ投入
df.to_sql(
    "classification",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print(f"{len(df)} rows imported.")