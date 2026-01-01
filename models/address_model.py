from database.db_connection import get_connection


def add_address(address_text):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO addresses (address)
    VALUES (%s)
    """

    cursor.execute(query, (address_text,))
    conn.commit()
    address_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return address_id


def get_all_addresses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM addresses ORDER BY address")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_address_by_id(address_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM addresses WHERE address_id = %s", (address_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
