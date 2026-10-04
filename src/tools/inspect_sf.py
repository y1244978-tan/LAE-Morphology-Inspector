# inspect_sf.py

import pandas as pd

df = pd.read_csv(
    "data/catalog_nonLAE_SF_F277W_with_err.txt",
    sep=r"\s+"
)

print(df.columns.tolist())
print("件数:", len(df))