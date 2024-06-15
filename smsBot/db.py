import sqlite3

DATABASE_NAME = "bot_data.db"


def init_db():
    """Initialize the database and create the necessary tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS secret_keys (
            id INTEGER PRIMARY KEY,
            uuid TEXT,
            secret_key TEXT,
            device_name TEXT
        )
        '''
    )
    conn.commit()
    conn.close()


def set_secret_key_for_uuid(uuid, secret_key, device_name):
    """Store the secret key and device name for a given uuid if not already present."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT OR IGNORE INTO secret_keys (uuid, secret_key, device_name) VALUES (?, ?, ?)", (uuid, secret_key, device_name))
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
    """Retrieve all secret keys and device names for a given uuid."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT secret_key, device_name FROM secret_keys WHERE uuid = ?", (uuid,))
    results = c.fetchall()
    conn.close()
    return results if results else []


def delete_specific_secret_key(uuid, secret_key):
    """Delete a specific secret key for a given uuid."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "DELETE FROM secret_keys WHERE uuid = ? AND secret_key = ?", (uuid, secret_key))
    conn.commit()
    conn.close()


def get_device_name_by_secret_key(secret_key):
    """Retrieve the device name for a given secret key."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT device_name FROM secret_keys WHERE secret_key = ?", (secret_key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
