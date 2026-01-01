from database.db_connection import get_connection


def add_customer(name, phone, address=None, remarks=None, image_path=None, address_id=None, village_id=None, entry_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    # Insert including optional address_id, village_id and entry_date (DB must be migrated)
    query = """
    INSERT INTO customers (name, phone, address, remarks, image_path, address_id, village_id, entry_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (name, phone, address, remarks, image_path, address_id, village_id, entry_date))
    conn.commit()

    customer_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return customer_id

def get_all_customers():
    """
    Fetch all customers (includes village name if available)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT c.*, v.name AS village_name, a.address AS address_text
    FROM customers c
    LEFT JOIN villages v ON c.village_id = v.village_id
    LEFT JOIN addresses a ON c.address_id = a.address_id
    ORDER BY COALESCE(c.entry_date, c.created_at) DESC
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT c.*, v.name AS village_name, a.address AS address_text
    FROM customers c
    LEFT JOIN villages v ON c.village_id = v.village_id
    LEFT JOIN addresses a ON c.address_id = a.address_id
    WHERE c.customer_id = %s
    """

    cursor.execute(query, (customer_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def update_customer(customer_id, name, phone, address=None, remarks=None, address_id=None, village_id=None, entry_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE customers
    SET name=%s, phone=%s, address=%s, remarks=%s, address_id=%s, village_id=%s, entry_date=%s
    WHERE customer_id=%s
    """

    cursor.execute(query, (name, phone, address, remarks, address_id, village_id, entry_date, customer_id))
    conn.commit()

    cursor.close()
    conn.close()

def delete_customer(customer_id):
    """
    Delete customer (guarantors & items auto-delete via FK)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE customer_id = %s",
        (customer_id,)
    )
    conn.commit()

    cursor.close()
    conn.close()



def insert_customer(name, phone, address, remarks, entry_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO customers (name, phone, address, remarks, entry_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (name, phone, address, remarks, entry_date))
    conn.commit()

    cursor.close()
    conn.close()
