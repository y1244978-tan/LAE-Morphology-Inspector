from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO classification (
    id,
    image_family,
    image_subset,
    logM,
    Re,
    Re_err,
    concentration,
    concentration_err,
    asymmetry,
    asymmetry_err,
    detectable,
    bright_neighbor,
    multiple_component,
    point_source,
    memo
)
VALUES (
    123456,
    'images',
    'LAE_A',
    8.5,
    1.2,
    0.1,
    3.0,
    0.2,
    0.4,
    0.1,
    1,
    0,
    0,
    0,
    'test'
)
""")

conn.commit()
conn.close()

print("saved.")
