import os
import sys

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.db_connection import get_connection


# -------------------------------
# Utility Functions
# -------------------------------

def table_exists(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
            """,
            (conn.database, table_name)
        )
        return cursor.fetchone()[0] > 0


def column_exists(conn, table_name, column_name):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = %s 
              AND table_name = %s 
              AND column_name = %s
            """,
            (conn.database, table_name, column_name)
        )
        return cursor.fetchone()[0] > 0


def execute_query(conn, query, message):
    with conn.cursor() as cursor:
        cursor.execute(query)
    print(message)


# -------------------------------
# Migration Logic
# -------------------------------

def run_migration():
    conn = get_connection()

    try:
        print("\n🚀 Starting Database Migration...\n")

        # -------------------------------
        # Tables Creation
        # -------------------------------

        if not table_exists(conn, "addresses"):
            execute_query(conn, """
                CREATE TABLE addresses (
                    address_id INT AUTO_INCREMENT PRIMARY KEY,
                    address TEXT
                )
            """, "✅ Created table: addresses")
        else:
            print("⚠️  Table already exists: addresses")

        if not table_exists(conn, "villages"):
            execute_query(conn, """
                CREATE TABLE villages (
                    village_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                )
            """, "✅ Created table: villages")
        else:
            print("⚠️  Table already exists: villages")

        # -------------------------------
        # Customers Table Updates
        # -------------------------------

        if not column_exists(conn, "customers", "address_id"):
            execute_query(conn,
                "ALTER TABLE customers ADD COLUMN address_id INT NULL",
                "✅ Added: customers.address_id"
            )
        else:
            print("⚠️  Column exists: customers.address_id")

        if not column_exists(conn, "customers", "village_id"):
            execute_query(conn,
                "ALTER TABLE customers ADD COLUMN village_id INT NULL",
                "✅ Added: customers.village_id"
            )
        else:
            print("⚠️  Column exists: customers.village_id")

        if not column_exists(conn, "customers", "entry_date"):
            execute_query(conn,
                "ALTER TABLE customers ADD COLUMN entry_date DATE NULL",
                "✅ Added: customers.entry_date"
            )
        else:
            print("⚠️  Column exists: customers.entry_date")

        # -------------------------------
        # Items Table Updates
        # -------------------------------

        if not column_exists(conn, "items", "interest_type"):
            execute_query(conn,
                "ALTER TABLE items ADD COLUMN interest_type VARCHAR(20) DEFAULT 'PERCENT' NULL",
                "✅ Added: items.interest_type"
            )
        else:
            print("⚠️  Column exists: items.interest_type")

        if not column_exists(conn, "items", "serial_no"):
            execute_query(conn,
                "ALTER TABLE items ADD COLUMN serial_no VARCHAR(255) NULL",
                "✅ Added: items.serial_no"
            )
        else:
            print("⚠️  Column exists: items.serial_no")

        if not column_exists(conn, "items", "invoice_no"):
            execute_query(conn,
                "ALTER TABLE items ADD COLUMN invoice_no VARCHAR(255) NULL",
                "✅ Added: items.invoice_no"
            )
        else:
            print("⚠️  Column exists: items.invoice_no")

        if not column_exists(conn, "items", "status"):
            execute_query(conn,
                "ALTER TABLE items ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE' NULL",
                "✅ Added: items.status"
            )
        else:
            print("⚠️  Column exists: items.status")

        conn.commit()
        print("\n🎉 Migration Completed Successfully!\n")

    except Exception as e:
        conn.rollback()
        print("\n❌ Migration Failed:", e)

    finally:
        conn.close()


# -------------------------------
# Entry Point
# -------------------------------

if __name__ == "__main__":
    run_migration()