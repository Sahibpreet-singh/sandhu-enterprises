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
            i.item_id,
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


def search_customer_items(filters=None):
    """Search customer items with optional filters.

    Supported filters (dict keys):
    - name: partial match against customer name
    - phone: partial match against customer phone
    - village: partial match against village name
    - address: partial match against customer address
    - item: partial match against item brand/model
    - status: 'Paid' | 'Unpaid' | 'All' (default 'All')
    - due_min: minimum due amount (numeric)
    - due_max: maximum due amount (numeric)
    - payment_from: payment date from (YYYY-MM-DD)
    - payment_to: payment date to (YYYY-MM-DD)

    Returns list of dict rows including computed fields: total_paid, due_amount, paid_status
    """
    filters = filters or {}
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query: include a subquery to sum payments per item
    query = """
        SELECT
            c.customer_id,
            c.name AS customer_name,
            c.phone AS customer_phone,
            COALESCE(a.address, c.address) AS customer_address,
            c.remarks AS customer_remarks,
            i.item_id,
            i.brand,
            i.model,
            i.item_amount,
            i.installment_mode,
            i.total_installments,
            IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0) AS total_paid,
            (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) AS due_amount,
            CASE WHEN (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) <= 0 THEN 'Paid' ELSE 'Unpaid' END AS paid_status,
            v.name AS village_name,
            (SELECT MAX(payment_date) FROM payments p2 WHERE p2.item_id = i.item_id) AS last_payment_date
        FROM customers c
        LEFT JOIN items i ON c.customer_id = i.customer_id
        LEFT JOIN villages v ON c.village_id = v.village_id
        LEFT JOIN addresses a ON c.address_id = a.address_id
        WHERE 1=1
    """

    params = []

    # Dynamic filters
    if filters.get("name"):
        query += " AND LOWER(c.name) LIKE %s"
        params.append(f"%{filters['name'].lower()}%")
    if filters.get("phone"):
        query += " AND LOWER(c.phone) LIKE %s"
        params.append(f"%{filters['phone'].lower()}%")
    if filters.get("village"):
        query += " AND LOWER(v.name) LIKE %s"
        params.append(f"%{filters['village'].lower()}%")
    if filters.get("address"):
        query += " AND LOWER(COALESCE(a.address, c.address, '')) LIKE %s"
        params.append(f"%{filters['address'].lower()}%")
    if filters.get("item"):
        query += " AND (LOWER(i.brand) LIKE %s OR LOWER(i.model) LIKE %s)"
        params.append(f"%{filters['item'].lower()}%")
        params.append(f"%{filters['item'].lower()}%")

    # status filter handled after computing due_amount, so use HAVING via wrapping subquery or recompute in SQL
    # Simpler: add conditions using the same subquery expression
    if filters.get("status") and filters.get("status") in ("Paid", "Unpaid"):
        if filters['status'] == "Paid":
            query += " AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) <= 0"
        else:
            query += " AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) > 0"

    if filters.get("due_min") is not None:
        query += " AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) >= %s"
        params.append(filters["due_min"])
    if filters.get("due_max") is not None:
        query += " AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) <= %s"
        params.append(filters["due_max"])

    # payment date range: include items that have any payment within the range
    if filters.get("payment_from"):
        query += " AND EXISTS (SELECT 1 FROM payments p3 WHERE p3.item_id = i.item_id AND p3.payment_date >= %s)"
        params.append(filters["payment_from"])
    if filters.get("payment_to"):
        query += " AND EXISTS (SELECT 1 FROM payments p4 WHERE p4.item_id = i.item_id AND p4.payment_date <= %s)"
        params.append(filters["payment_to"])

    query += " ORDER BY c.customer_id DESC, i.item_id DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
