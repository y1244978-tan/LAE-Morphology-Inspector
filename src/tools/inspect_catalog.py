import pandas as pd

print("START")

df = pd.read_csv(
    "data/catalog_LAE_F277W_with_err.txt",
    sep=r"\s+"
)

print("LOADED")

print("列名一覧")
print("-" * 30)

for col in df.columns:
    print(col)

print()
print(df.head())

print()
print("天体数:", len(df))

print("END")
