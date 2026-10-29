import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "database/LAE.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    """
    SELECT
        id,
        image_subset,
        detectable,
        bright_neighbor,
        multiple_component,
        point_source,
        memo,
        created_at
    FROM classification
    ORDER BY created_at
    """,
    conn
)

# ----------------
# 最新判定だけ残す
# ----------------

print("重複除去前 :", len(df))

df = df.sort_values(
    "created_at"
)

df = df.drop_duplicates(
    subset=["id"],
    keep="last"
)

print("重複除去後 :", len(df))
print(
    "ユニークID数 :",
    df["id"].nunique()
)

# 日付付きファイル名
today = datetime.now().strftime("%Y%m%d")

output_file = (
    f"output/morphology_labels_{today}.csv"
)

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"保存先: {output_file}")
print(f"総天体数: {len(df)}")

print("\n===== 集計 =====")

n = len(df)

detectable_n = df["detectable"].sum()
neighbor_n = df["bright_neighbor"].sum()
multiple_n = df["multiple_component"].sum()
point_n = df["point_source"].sum()

print(f"総天体数         : {n}")

print(
    f"Detectable       : "
    f"{detectable_n} "
    f"({100*detectable_n/n:.1f}%)"
)

print(
    f"Bright Neighbor  : "
    f"{neighbor_n} "
    f"({100*neighbor_n/n:.1f}%)"
)

print(
    f"Multiple Comp.   : "
    f"{multiple_n} "
    f"({100*multiple_n/n:.1f}%)"
)

print(
    f"Point Source     : "
    f"{point_n} "
    f"({100*point_n/n:.1f}%)"
)

conn.close()
