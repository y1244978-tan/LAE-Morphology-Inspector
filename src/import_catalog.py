import sqlite3
import pandas as pd
import numpy as np

catalogs = [
    (
        "data/catalog_LAE_F277W_with_err_kpc.txt",
        "LAE"
    ),
    (
        "data/catalog_nonLAE_SF_F277W_with_err_kpc.txt",
        "SF"
    ),
    (
        "data/catalog_nonLAE_Q_F277W_with_err_kpc.txt",
        "Q"
    )
]

conn = sqlite3.connect("database/LAE.db")

conn.execute("""
DROP TABLE IF EXISTS galaxy
""")

for catalog_file, sample_name in catalogs:

    df = pd.read_csv(
        catalog_file,
        sep=r"\s+",
        encoding="cp932"
    )

    if "EW" in df.columns:
        ew_values = df["EW"]
    else:
        ew_values = None

    galaxy_df = pd.DataFrame({
        "id": df["ID"],
        "sample": sample_name,

        "ew": ew_values,

        "logM": np.log10(df["Ms_med"]),

        "Re": df["Re"],
        "Re_err": df["Re_err"],

        "concentration": df["C_1sig/C_n2p5"],
        "concentration_err": df["C_err"],

        "asymmetry": df["A_1sig"],
        "asymmetry_err": df["A_err"]
    })

    galaxy_df = galaxy_df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    galaxy_df.to_sql(
        "galaxy",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"{sample_name}: {len(galaxy_df)} imported."
    )

conn.close()

print("finished.")