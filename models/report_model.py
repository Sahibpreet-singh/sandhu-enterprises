from database.db_connection import get_connection


def _build_installment_cases_query(filters=None):
    """
    Build query and params for installment case listing.

    Returns rows with UI-friendly aliases:
    file_no, entry_date, customer_name, customer_address, village_name,
    mobile_no, finance_amount, balance, item_id, customer_id, brand, model,
    installment_amount, total_installments, installment_mode, paid_status,
    total_paid, due_amount, overdue_days
    """
    filters = filters or {}

    query = """
        SELECT
            COALESCE(NULLIF(i.invoice_no, ''), CONCAT('C', c.customer_id, '-I', i.item_id)) AS file_no,
            COALESCE(c.entry_date, i.start_date) AS entry_date,
            c.customer_id,
            i.item_id,
            c.name AS customer_name,
            COALESCE(a.address, c.address, '') AS customer_address,
            v.name AS village_name,
            c.phone AS mobile_no,
            c.phone AS customer_phone,
            i.brand,
            i.model,
            COALESCE(i.finance_amount, i.item_amount, 0) AS finance_amount,
            GREATEST(
                COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0),
                0
            ) AS balance,
            i.installment_amount,
            i.total_installments,
            i.installment_mode,
            IFNULL(pay.total_paid, 0) AS total_paid,
            GREATEST(
                COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0),
                0
            ) AS due_amount,
            CASE
                WHEN GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0
                    OR UPPER(COALESCE(i.status, '')) = 'CLOSED' THEN 'Paid'
                WHEN IFNULL(pay.total_paid, 0) > 0 THEN 'Partial'
                ELSE 'Unpaid'
            END AS paid_status,
            CASE
                WHEN i.start_date IS NULL
                     OR COALESCE(i.installment_amount, 0) <= 0
                     OR GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0
                THEN 0
                ELSE GREATEST(
                    DATEDIFF(
                        CURDATE(),
                        DATE_ADD(
                            i.start_date,
                            INTERVAL FLOOR(IFNULL(pay.total_paid, 0) / NULLIF(i.installment_amount, 0)) MONTH
                        )
                    ),
                    0
                )
            END AS overdue_days
        FROM items i
        JOIN customers c
            ON c.customer_id = i.customer_id
        LEFT JOIN villages v
            ON c.village_id = v.village_id
        LEFT JOIN addresses a
            ON c.address_id = a.address_id
        LEFT JOIN (
            SELECT
                p.item_id,
                SUM(p.amount_paid) AS total_paid,
                MAX(p.payment_date) AS last_payment_date
            FROM payments p
            GROUP BY p.item_id
        ) pay
            ON pay.item_id = i.item_id
        WHERE 1=1
    """

    params = []

    if filters.get("customer_name"):
        query += " AND LOWER(c.name) LIKE %s"
        params.append(f"%{filters['customer_name'].lower()}%")
    if filters.get("name"):
        query += " AND LOWER(c.name) LIKE %s"
        params.append(f"%{filters['name'].lower()}%")
    if filters.get("mobile_no"):
        query += " AND LOWER(COALESCE(c.phone, '')) LIKE %s"
        params.append(f"%{filters['mobile_no'].lower()}%")
    if filters.get("phone"):
        query += " AND LOWER(COALESCE(c.phone, '')) LIKE %s"
        params.append(f"%{filters['phone'].lower()}%")
    if filters.get("village"):
        query += " AND LOWER(COALESCE(v.name, '')) LIKE %s"
        params.append(f"%{filters['village'].lower()}%")
    if filters.get("address"):
        query += " AND LOWER(COALESCE(a.address, c.address, '')) LIKE %s"
        params.append(f"%{filters['address'].lower()}%")
    if filters.get("item"):
        query += " AND (LOWER(COALESCE(i.brand, '')) LIKE %s OR LOWER(COALESCE(i.model, '')) LIKE %s)"
        params.append(f"%{filters['item'].lower()}%")
        params.append(f"%{filters['item'].lower()}%")
    if filters.get("item_id"):
        query += " AND i.item_id = %s"
        params.append(filters["item_id"])
    if filters.get("customer_id"):
        query += " AND c.customer_id = %s"
        params.append(filters["customer_id"])
    if filters.get("status") in ("Paid", "Unpaid", "Partial"):
        if filters["status"] == "Paid":
            query += " AND (GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0 OR UPPER(COALESCE(i.status, '')) = 'CLOSED')"
        elif filters["status"] == "Partial":
            query += " AND IFNULL(pay.total_paid, 0) > 0 AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) > 0"
        else:
            query += " AND IFNULL(pay.total_paid, 0) <= 0 AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) > 0"
    if filters.get("due_min") is not None:
        query += " AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) >= %s"
        params.append(filters["due_min"])
    if filters.get("due_max") is not None:
        query += " AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= %s"
        params.append(filters["due_max"])
    if filters.get("entry_date_from"):
        query += " AND COALESCE(c.entry_date, i.start_date) >= %s"
        params.append(filters["entry_date_from"])
    if filters.get("entry_date_to"):
        query += " AND COALESCE(c.entry_date, i.start_date) <= %s"
        params.append(filters["entry_date_to"])

    query += """
        ORDER BY
            CASE
                WHEN GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) > 0 THEN 0
                ELSE 1
            END,
            CASE
                WHEN i.start_date IS NULL
                     OR COALESCE(i.installment_amount, 0) <= 0
                     OR GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0
                THEN 0
                ELSE GREATEST(
                    DATEDIFF(
                        CURDATE(),
                        DATE_ADD(
                            i.start_date,
                            INTERVAL FLOOR(IFNULL(pay.total_paid, 0) / NULLIF(i.installment_amount, 0)) MONTH
                        )
                    ),
                    0
                )
            END DESC,
            COALESCE(c.entry_date, i.start_date) DESC,
            i.item_id DESC
    """

    return query, params


def get_installment_cases(filters=None):
    """
    Fetch installment cases for list/grid screens.

    Supported filters include:
    - customer_name / name
    - mobile_no / phone
    - village
    - address
    - item
    - item_id
    - customer_id
    - status: Paid | Partial | Unpaid
    - due_min
    - due_max
    - entry_date_from
    - entry_date_to
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query, params = _build_installment_cases_query(filters)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


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
    - status: 'Paid' | 'Unpaid' | 'Partial' | 'All' (default 'All')
    - due_min: minimum due amount (numeric)
    - due_max: maximum due amount (numeric)
    - payment_from: payment date from (DD-MM-YYYY or YYYY-MM-DD)
    - payment_to: payment date to (DD-MM-YYYY or YYYY-MM-DD)

    Returns list of dict rows including computed fields:
    total_paid, due_amount, paid_status, file_no, entry_date, mobile_no,
    finance_amount, balance, overdue_days
    """
    filters = filters or {}
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            c.customer_id,
            c.name AS customer_name,
            c.phone AS customer_phone,
            c.phone AS mobile_no,
            COALESCE(a.address, c.address) AS customer_address,
            c.remarks AS customer_remarks,
            COALESCE(c.entry_date, i.start_date) AS entry_date,
            COALESCE(NULLIF(i.invoice_no, ''), CONCAT('C', c.customer_id, '-I', i.item_id)) AS file_no,
            i.item_id,
            i.brand,
            i.model,
            i.item_amount,
            i.finance_amount,
            i.installment_amount,
            i.installment_mode,
            i.total_installments,
            IFNULL(pay.total_paid, 0) AS total_paid,
            GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) AS due_amount,
            GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) AS balance,
            CASE
                WHEN GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0
                    OR UPPER(COALESCE(i.status, '')) = 'CLOSED' THEN 'Paid'
                WHEN IFNULL(pay.total_paid, 0) > 0 THEN 'Partial'
                ELSE 'Unpaid'
            END AS paid_status,
            v.name AS village_name,
            pay.last_payment_date,
            CASE
                WHEN i.start_date IS NULL
                     OR COALESCE(i.installment_amount, 0) <= 0
                     OR GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0
                THEN 0
                ELSE GREATEST(
                    DATEDIFF(
                        CURDATE(),
                        DATE_ADD(
                            i.start_date,
                            INTERVAL FLOOR(IFNULL(pay.total_paid, 0) / NULLIF(i.installment_amount, 0)) MONTH
                        )
                    ),
                    0
                )
            END AS overdue_days
        FROM customers c
        LEFT JOIN items i ON c.customer_id = i.customer_id
        LEFT JOIN villages v ON c.village_id = v.village_id
        LEFT JOIN addresses a ON c.address_id = a.address_id
        LEFT JOIN (
            SELECT
                p.item_id,
                SUM(p.amount_paid) AS total_paid,
                MAX(p.payment_date) AS last_payment_date
            FROM payments p
            GROUP BY p.item_id
        ) pay ON pay.item_id = i.item_id
        WHERE 1=1
    """

    params = []

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
        query += " AND (LOWER(COALESCE(i.brand, '')) LIKE %s OR LOWER(COALESCE(i.model, '')) LIKE %s)"
        params.append(f"%{filters['item'].lower()}%")
        params.append(f"%{filters['item'].lower()}%")

    if filters.get("status") and filters.get("status") in ("Paid", "Unpaid", "Partial"):
        if filters["status"] == "Paid":
            query += " AND (GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= 0 OR UPPER(COALESCE(i.status, '')) = 'CLOSED')"
        elif filters["status"] == "Partial":
            query += " AND IFNULL(pay.total_paid, 0) > 0 AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) > 0"
        else:
            query += " AND IFNULL(pay.total_paid, 0) <= 0 AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) > 0"

    if filters.get("due_min") is not None:
        query += " AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) >= %s"
        params.append(filters["due_min"])
    if filters.get("due_max") is not None:
        query += " AND GREATEST(COALESCE(i.finance_amount, i.item_amount, 0) - IFNULL(pay.total_paid, 0), 0) <= %s"
        params.append(filters["due_max"])

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

    for row in rows:
        row["finance_amount"] = row.get("finance_amount") or row.get("item_amount") or 0

    return rows