from database.db_connection import get_connection


def add_item(
    customer_id,
    brand,
    model,
    serial_no,
    invoice_no,
    item_amount,
    advance_amount,
    finance_amount,
    interest_rate,
    installment_mode,
    total_installments,
    installment_amount,
    start_date
):
    """
    Add a financed item for a customer
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO items (
        customer_id,
        brand,
        model,
        serial_no,
        invoice_no,
        item_amount,
        advance_amount,
        finance_amount,
        interest_rate,
        installment_mode,
        total_installments,
        installment_amount,
        start_date,
        status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVE')
    """

    cursor.execute(query, (
        customer_id,
        brand,
        model,
        serial_no,
        invoice_no,
        item_amount,
        advance_amount,
        finance_amount,
        interest_rate,
        installment_mode,
        total_installments,
        installment_amount,
        start_date
    ))

    conn.commit()
    item_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return item_id


def get_items_by_customer(customer_id):
    """
    Fetch all items purchased by a customer
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM items WHERE customer_id = %s",
        (customer_id,)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_item_by_id(item_id):
    """
    Fetch single item
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM items WHERE item_id = %s",
        (item_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def update_item_status(item_id, status):
    """
    Update item status (ACTIVE / CLOSED)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE items SET status = %s WHERE item_id = %s",
        (status, item_id)
    )

    conn.commit()

    cursor.close()
    conn.close()
