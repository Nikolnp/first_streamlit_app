import sqlite3

DB_PATH = "sustainability.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS emissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        electricity REAL,
        water REAL,
        car_km REAL,
        diet TEXT,
        monthly_total REAL,
        yearly_total REAL
    )
    """)

    conn.commit()
    conn.close()


def save_user_and_emissions(user_id, name, email,
                             electricity, water, car_km, diet,
                             monthly_total, yearly_total):

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO users (user_id, name, email)
        VALUES (?, ?, ?)
    """, (user_id, name, email))

    c.execute("""
        UPDATE users
        SET name = ?, email = ?
        WHERE email = ?
    """, (name, email, email))

    c.execute("""
        INSERT INTO emissions (
            user_id, electricity, water, car_km, diet, monthly_total, yearly_total
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, electricity, water, car_km, diet, monthly_total, yearly_total
    ))

    conn.commit()
    conn.close()


def load_emissions():
    conn = get_connection()
    import pandas as pd
    df = pd.read_sql("SELECT * FROM emissions", conn)
    conn.close()
    return df
