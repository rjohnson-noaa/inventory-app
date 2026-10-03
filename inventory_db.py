import sqlite3

DB_NAME = "inventory.db"


def init_db():
    """Create the table if it does not already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def add_item_db(name, quantity, price):
    """Insert a new record into SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price),
    )
    conn.commit()
    conn.close()


def fetch_all_items():
    """Retrieve all items from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity, price FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_item_db(item_id):
    """Delete a record by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()