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
    start_date,
    interest_type='PERCENT'
):
    """
    Add a financed item for a customer
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Validate interest_rate early so we get a clear error before DB insertion
    try:
        interest_rate = float(interest_rate)
    except (TypeError, ValueError):
        raise ValueError("Invalid interest_rate: must be a number")

    # If percent, expect 0-100; if absolute amount, ensure non-negative
    if str(interest_type).upper().startswith('P'):
        if not (0 <= interest_rate <= 100):
            raise ValueError("Interest rate (percent) must be between 0 and 100")
    else:
        if interest_rate < 0:
            raise ValueError("Interest amount must be non-negative")

    # Round to 2 decimal places for storage
    interest_rate = round(interest_rate, 2)

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
        interest_type,
        installment_mode,
        total_installments,
        installment_amount,
        start_date,
        status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVE')
    """

    try:
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
            interest_type,
            installment_mode,
            total_installments,
            installment_amount,
            start_date
        ))
    except Exception as e:
        # Surface a clearer message if the DB reports an out-of-range value
        if 'Out of range' in str(e) or '1264' in str(e):
            raise ValueError(f"Database error: out of range value for interest_rate ({interest_rate}). Check DB column type and precision.") from e
        raise

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
