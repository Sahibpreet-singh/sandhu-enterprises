from database.db_connection import get_connection
from models.item_model import update_item_status


def get_last_remaining_amount(item_id):
    """
    Get remaining amount from last payment.
    If no payment exists, return full payable amount.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT remaining_amount
        FROM payments
        WHERE item_id = %s
        ORDER BY payment_date DESC
        LIMIT 1
        """,
        (item_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row[0] if row else None


def add_payment(item_id, payment_date, amount_paid, total_payable):
    """
    Add EMI payment and update remaining balance
    """
    last_remaining = get_last_remaining_amount(item_id)

    if last_remaining is None:
        remaining_amount = total_payable - amount_paid
    else:
        remaining_amount = last_remaining - amount_paid

    if remaining_amount < 0:
        raise Exception("Payment exceeds remaining amount")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO payments (
        item_id,
        payment_date,
        amount_paid,
        remaining_amount
    )
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (
        item_id,
        payment_date,
        amount_paid,
        remaining_amount
    ))

    conn.commit()

    if remaining_amount == 0:
        update_item_status(item_id, "CLOSED")

    cursor.close()
    conn.close()

    return remaining_amount


def get_payments_by_item(item_id):
    """
    Fetch EMI payment history for an item
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM payments WHERE item_id = %s ORDER BY payment_date",
        (item_id,)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
