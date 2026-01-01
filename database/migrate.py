import os
import sys

# Ensure project root is on sys.path so package imports like `database.*` work when
# the script is executed directly (python database/migrate.py) or via `-m`.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.db_connection import get_connection


def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s",
        (conn.database, table_name)
    )
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    return exists


def column_exists(conn, table_name, column_name):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND column_name = %s",
        (conn.database, table_name, column_name)
    )
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    return exists


def run_migration():
    conn = get_connection()
    try:
        # Addresses table
        if not table_exists(conn, 'addresses'):
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE addresses (
                    address_id INT AUTO_INCREMENT PRIMARY KEY,
                    address TEXT
                )
                """
            )
            cur.close()
            print('Created table: addresses')
        else:
            print('Table already exists: addresses')

        # Villages table
        if not table_exists(conn, 'villages'):
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE villages (
                    village_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                )
                """
            )
            cur.close()
            print('Created table: villages')
        else:
            print('Table already exists: villages')

        # Add columns to customers if missing
        if not column_exists(conn, 'customers', 'address_id'):
            cur = conn.cursor()
            cur.execute("ALTER TABLE customers ADD COLUMN address_id INT NULL")
            cur.close()
            print('Added column: customers.address_id')
        else:
            print('Column already exists: customers.address_id')

        if not column_exists(conn, 'customers', 'village_id'):
            cur = conn.cursor()
            cur.execute("ALTER TABLE customers ADD COLUMN village_id INT NULL")
            cur.close()
            print('Added column: customers.village_id')
        else:
            print('Column already exists: customers.village_id')

        if not column_exists(conn, 'customers', 'entry_date'):
            cur = conn.cursor()
            cur.execute("ALTER TABLE customers ADD COLUMN entry_date DATE NULL")
            cur.close()
            print('Added column: customers.entry_date')
        else:
            print('Column already exists: customers.entry_date')

        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    print('Running DB migration...')
    try:
        run_migration()
        print('Migration completed.')
    except Exception as e:
        print('Migration failed:', e)
