from database.db_connection import get_connection

def add_customer(name,phone,address,remarks=None,image_path=None):
    conn =get_connection()
    cursor= conn.cursor()

    query = """
    INSERT INTO customers (name, phone, address, remarks, image_path)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (name, phone, address, remarks, image_path))
    conn.commit()

    customer_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return customer_id

def get_all_customers():
    """
    Fetch all customers
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers ORDER BY created_at DESC")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_customer_by_id(customer_id):
    """
    Fetch single customer by ID
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM customers WHERE customer_id = %s",
        (customer_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def update_customer(customer_id, name, phone, address, remarks=None):
    """
    Update customer details
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE customers
    SET name=%s, phone=%s, address=%s, remarks=%s
    WHERE customer_id=%s
    """

    cursor.execute(query, (name, phone, address, remarks, customer_id))
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



def insert_customer(name, phone, address, remarks):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO customers (name, phone, address, remarks)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (name, phone, address, remarks))
    conn.commit()

    cursor.close()
    conn.close()
