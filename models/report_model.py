from database.db_connection import get_connection


def get_all_customer_items():
    """
    Fetch ALL customers with:
    - Full customer info
    - Item/EMI info if available
    - Guarantor info if available
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            c.customer_id,
            c.name AS customer_name,
            c.phone AS customer_phone,
            COALESCE(a.address, c.address) AS customer_address,
            c.remarks AS customer_remarks,
            i.brand,
            i.model,
            i.item_amount,
            i.advance_amount,
            i.finance_amount,
            i.interest_rate,
            i.installment_amount,
            i.installment_mode,
            i.total_installments,
            g.name AS guarantor_name,
            g.phone AS guarantor_phone,
            g.address AS guarantor_address,
            v.name AS village_name
        FROM customers c
        LEFT JOIN items i
            ON c.customer_id = i.customer_id
        LEFT JOIN guarantors g
            ON c.customer_id = g.customer_id
        LEFT JOIN villages v
            ON c.village_id = v.village_id
        LEFT JOIN addresses a
            ON c.address_id = a.address_id
        ORDER BY c.customer_id DESC, g.guarantor_id ASC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
