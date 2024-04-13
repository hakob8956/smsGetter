# db.py
import sqlite3

DATABASE_NAME = "bot_data.db"


def init_db():
    """Initialize the database and create the necessary tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS secret_keys (uuid TEXT PRIMARY KEY, secret_key TEXT)''')
    conn.commit()
    conn.close()


def set_secret_key_for_uuid(uuid, secret_key):
    """Store the secret key for a given uuid if not already present."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT OR IGNORE INTO secret_keys (uuid, secret_key) VALUES (?, ?)", (uuid, secret_key))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Record already exists. No new record added.")
    finally:
        conn.close()


def get_uuids_for_secret_key(secret_key):
    """Retrieve all uuids for a given secret key, if they exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT uuid FROM secret_keys WHERE secret_key = ?", (secret_key,))
    results = c.fetchall()
    conn.close()
    return [result[0] for result in results] if results else []


def delete_all_secret_keys(uuid):
    """Delete all secret keys for a given uuid."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM secret_keys WHERE uuid = ?", (uuid,))
    conn.commit()
    conn.close()


def get_secret_keys_by_uuid(uuid):
    """Retrieve all secret keys for a given uuid."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT secret_key FROM secret_keys WHERE uuid = ?", (uuid,))
    results = c.fetchall()
    conn.close()
    return [result[0] for result in results] if results else []


def delete_specific_secret_key(uuid, secret_key):
    """Delete a specific secret key for a given uuid."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "DELETE FROM secret_keys WHERE uuid = ? AND secret_key = ?", (uuid, secret_key))
    conn.commit()
    conn.close()
