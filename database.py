# redesigned `database.py`

import sqlite3
import pandas as pd
import streamlit as st
import uuid


DB_PATH = "sustainability.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        # enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    except Exception as e:

        st.error(f"Database connection failed: {e}")

        return None


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    conn = get_connection()

    if conn is None:
        return

    try:

        c = conn.cursor()

        # -------------------------------------------------
        # USERS TABLE
        # -------------------------------------------------
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (

            user_id TEXT PRIMARY KEY,

            email TEXT UNIQUE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # -------------------------------------------------
        # EMISSIONS TABLE
        # -------------------------------------------------
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

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(user_id)
        )
        """)

        conn.commit()

    except Exception as e:

        st.error(f"Database initialization failed: {e}")

    finally:

        conn.close()


# =========================================================
# USER LOOKUP
# =========================================================

def get_user_id_by_email(email):

    conn = get_connection()

    if conn is None:
        return None

    try:

        c = conn.cursor()

        c.execute(
            "SELECT user_id FROM users WHERE email = ?",
            (email,)
        )

        result = c.fetchone()

        if result:
            return result[0]

        return None

    except Exception as e:

        st.error(f"User lookup failed: {e}")

        return None

    finally:

        conn.close()


# =========================================================
# EMAIL EXISTS CHECK
# =========================================================

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


# =========================================================
# SAVE USER + EMISSIONS
# =========================================================

def save_user(user_dict):

    conn = get_connection()

    if conn is None:
        return False

    try:

        c = conn.cursor()

        # -------------------------------------------------
        # CHECK IF USER EXISTS
        # -------------------------------------------------
        existing_user_id = get_user_id_by_email(
            user_dict["email"]
        )

        # -------------------------------------------------
        # CREATE NEW UUID IF NEW USER
        # -------------------------------------------------
        if existing_user_id is None:

            user_id = str(uuid.uuid4())

            c.execute("""
                INSERT INTO users (
                    user_id,
                    email
                )
                VALUES (?, ?)
            """, (
                user_id,
                user_dict["email"]
            ))

        else:

            user_id = existing_user_id

        # -------------------------------------------------
        # INSERT EMISSIONS EVENT
        # -------------------------------------------------
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
            user_dict["electricity"],
            user_dict["water"],
            user_dict["car_km"],
            user_dict["diet"],
            user_dict["monthly_total"],
            user_dict["yearly_total"]
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


# =========================================================
# LOAD ALL EMISSIONS
# =========================================================

def load_emissions():

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    try:

        query = """
        SELECT
            e.id,
            e.user_id,
            e.electricity,
            e.water,
            e.car_km,
            e.diet,
            e.monthly_total,
            e.yearly_total,
            e.created_at
        FROM emissions e
        ORDER BY e.created_at DESC
        """

        df = pd.read_sql(query, conn)

        return df

    except Exception as e:

        st.error(f"Loading emissions failed: {e}")

        return pd.DataFrame()

    finally:

        conn.close()


# =========================================================
# ANALYTICS DATASET
# =========================================================

def get_emissions_analytics():

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    try:

        query = """
        SELECT
            u.user_id,
            u.email,
            e.monthly_total,
            e.yearly_total,
            e.created_at
        FROM users u
        JOIN emissions e
            ON u.user_id = e.user_id
        ORDER BY e.created_at DESC
        """

        df = pd.read_sql(query, conn)

        return df

    except Exception as e:

        st.error(f"Analytics load failed: {e}")

        return pd.DataFrame()

    finally:

        conn.close()

#def get_all_users():
    

