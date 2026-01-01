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


from decimal import Decimal, ROUND_HALF_UP


def add_payment(item_id, payment_date, amount_paid, total_payable):
    """
    Add EMI payment and update remaining balance.

    Coerce numeric values to Decimal to avoid mixing float and Decimal which
    causes TypeError during arithmetic.
    """
    last_remaining = get_last_remaining_amount(item_id)

    # Normalize inputs to Decimal using string conversion to avoid binary float issues
    amount_paid_d = Decimal(str(amount_paid))

    if last_remaining is None:
        total_payable_d = Decimal(str(total_payable))
        remaining = total_payable_d - amount_paid_d
    else:
        last_remaining_d = Decimal(str(last_remaining))
        remaining = last_remaining_d - amount_paid_d

    if remaining < Decimal('0'):
        raise Exception("Payment exceeds remaining amount")

    # Round to 2 decimal places for storage/display
    remaining = remaining.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

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

    # Use float for DB insertion to match existing numeric column types
    cursor.execute(query, (
        item_id,
        payment_date,
        float(amount_paid_d),
        float(remaining)
    ))

    conn.commit()

    if remaining == Decimal('0.00'):
        update_item_status(item_id, "CLOSED")

    cursor.close()
    conn.close()

    # Return remaining as Decimal (caller can format as needed)
    return remaining


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
