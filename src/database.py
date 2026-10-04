import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "database/LAE.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_history(galaxy_id):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM classification
        WHERE id = ?
        ORDER BY created_at DESC
        """,
        conn,
        params=(galaxy_id,)
    )

    conn.close()

    return df

def save_classification(data):

    conn = get_connection()

    cursor = conn.cursor()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    data = data + (created_at,)

    print("len(data) =", len(data))
    print(data)

    cursor.execute(
        """
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
            memo,
            created_at
        )
        VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?
        )
        """,
        data
    )

    conn.commit()
    conn.close()


def get_saved_ids(
    image_family,
    image_subset
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM classification
        WHERE image_family = ?
        AND image_subset = ?
    """, (
        image_family,
        image_subset
    ))

    ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return ids

def get_lae_by_ew(min_ew):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM galaxy
        WHERE sample='LAE'
        AND ew >= ?
        ORDER BY ew DESC
        """,
        conn,
        params=(min_ew,)
    )

    conn.close()

    return df

def get_sample_statistics():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            sample,
            COUNT(*) AS n,
            AVG(Re) AS mean_re,
            AVG(logM) AS mean_logM,
            AVG(concentration) AS mean_c,
            AVG(asymmetry) AS mean_a
        FROM galaxy
        GROUP BY sample
        """,
        conn
    )

    conn.close()

    return df

def get_classification_statistics():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            COUNT(*) AS total,
            SUM(detectable) AS detectable,
            SUM(bright_neighbor) AS bright_neighbor,
            SUM(multiple_component) AS multiple_component,
            SUM(point_source) AS point_source
        FROM classification
        """,
        conn
    )

    conn.close()

    return df

def get_classified_ids():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT c.id
        FROM classification c
        INNER JOIN galaxy g
        ON c.id = g.id
        ORDER BY c.id
        """,
        conn
    )

    conn.close()

    return df["id"].tolist()

def get_ranked_galaxies(
    sample,
    metric,
    order,
    limit_num
):
    conn = get_connection()

    query = f"""
    SELECT *
    FROM galaxy
    WHERE sample = ?
    ORDER BY {metric} {order}
    LIMIT ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(
            sample,
            limit_num
        )
    )

    conn.close()

    return df

def get_sampled_galaxies(
    sample,
    metric,
    high_n=10,
    mid_n=20,
    low_n=10
):
    conn = get_connection()

    query = """
    SELECT
        id,
        sample,
        ew,
        logM,
        Re,
        Re_err,
        concentration,
        concentration_err,
        asymmetry,
        asymmetry_err
    FROM galaxy
    WHERE sample = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(sample,)
    )

    conn.close()

    metric_map = {
        "Re": "Re",
        "concentration": "concentration",
        "asymmetry": "asymmetry",
        "logM": "logM",
        "ew": "ew"
    }

    metric_col = metric_map[metric]

    df = df.sort_values(
        metric_col
    ).reset_index(
        drop=True
    )

    n_total = len(df)

    low_df = df.iloc[
        : n_total // 3
    ]

    mid_df = df.iloc[
        n_total // 3 :
        2 * n_total // 3
    ]

    high_df = df.iloc[
        2 * n_total // 3 :
    ]

    low_sample = low_df.sample(
        n=min(
            low_n,
            len(low_df)
        ),
        random_state=42
    )

    mid_sample = mid_df.sample(
        n=min(
            mid_n,
            len(mid_df)
        ),
        random_state=42
    )

    high_sample = high_df.sample(
        n=min(
            high_n,
            len(high_df)
        ),
        random_state=42
    )

    sampled_df = pd.concat(
        [
            high_sample,
            mid_sample,
            low_sample
        ]
    )

    return sampled_df.reset_index(
        drop=True
    )
