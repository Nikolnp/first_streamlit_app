import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = "sustainability.db"


def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None


def init_db():
    conn = get_connection()

    if conn is None:
        return

    try:
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
            yearly_total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

    except Exception as e:
        conn.rollback()
        st.error(f"Database initialization failed: {e}")

    finally:
        conn.close()


def save_user_and_emissions(
    user_id,
    name,
    email,
    electricity,
    water,
    car_km,
    diet,
    monthly_total,
    yearly_total
):

    conn = get_connection()

    if conn is None:
        return False

    try:
        c = conn.cursor()

        # Insert or update user
        c.execute("""
            INSERT OR IGNORE INTO users (user_id, name, email)
            VALUES (?, ?, ?)
        """, (user_id, name, email))


        c.execute("""
            UPDATE users
            SET name = ?, email = ?
            WHERE user_id = ?
        """, (name, email, user_id))


        # Insert emissions record
        c.execute("""
            INSERT INTO emissions (
                user_id,
                electricity,
                water,
                car_km,
                diet,
                monthly_total,
                yearly_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            electricity,
            water,
            car_km,
            diet,
            monthly_total,
            yearly_total
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError as e:
        conn.rollback()
        st.error(f"Integrity error: {e}")
        return False

    except Exception as e:
        conn.rollback()
        st.error(f"Insert failed: {e}")
        return False

    finally:
        conn.close()


def load_emissions():

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    try:
        df = pd.read_sql("SELECT * FROM emissions ORDER BY created_at DESC", conn)
        return df

    except Exception as e:
        st.error(f"Loading emissions failed: {e}")
        return pd.DataFrame()

    finally:
        conn.close()


def email_exists(email):

    conn = get_connection()

    if conn is None:
        return False

    try:
        c = conn.cursor()

        c.execute(
            "SELECT 1 FROM users WHERE email = ? LIMIT 1",
            (email,)
        )

        result = c.fetchone()

        return result is not None

    except Exception as e:
        st.error(f"Email lookup failed: {e}")
        return False

    finally:
        conn.close()


def get_all_users():

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    try:
        df = pd.read_sql("SELECT * FROM users", conn)
        return df

    except Exception as e:
        st.error(f"User load failed: {e}")
        return pd.DataFrame()

    finally:
        conn.close()
