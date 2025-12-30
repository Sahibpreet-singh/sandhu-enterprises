from database.db_connection import get_connection


def add_guarantor(customer_id, name, phone, address):
    """
    Add a guarantor for a customer
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO guarantors (customer_id, name, phone, address)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (customer_id, name, phone, address))
    conn.commit()

    guarantor_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return guarantor_id


def get_guarantors_by_customer(customer_id):
    """
    Fetch all guarantors for a customer
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM guarantors WHERE customer_id = %s",
        (customer_id,)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def count_guarantors(customer_id):
    """
    Count guarantors for validation (max 2 allowed)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM guarantors WHERE customer_id = %s",
        (customer_id,)
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count


def delete_guarantor(guarantor_id):
    """
    Delete a guarantor
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM guarantors WHERE guarantor_id = %s",
        (guarantor_id,)
    )
    conn.commit()

    cursor.close()
    conn.close()
