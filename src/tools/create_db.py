import sqlite3

conn = sqlite3.connect("database/LAE.db")
cursor = conn.cursor()

# classification
cursor.execute("""
CREATE TABLE IF NOT EXISTS classification (
    id INTEGER,
    image_family TEXT,
    image_subset TEXT,

    logM REAL,

    Re REAL,
    Re_err REAL,

    concentration REAL,
    concentration_err REAL,

    asymmetry REAL,
    asymmetry_err REAL,

    detectable INTEGER,
    bright_neighbor INTEGER,
    multiple_component INTEGER,
    point_source INTEGER,

    memo TEXT
)
""")

# galaxy
cursor.execute("""
CREATE TABLE IF NOT EXISTS galaxy (
    id INTEGER,
    sample TEXT,

    ew REAL,

    logM REAL,

    Re REAL,
    Re_err REAL,

    concentration REAL,
    concentration_err REAL,

    asymmetry REAL,
    asymmetry_err REAL
)
""")

conn.commit()
conn.close()

print("classification table created.")
print("galaxy table created.")