-- All SQL parts from the project

-- From database/schema.sql
CREATE TABLE IF NOT EXISTS addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    address TEXT
);

CREATE TABLE IF NOT EXISTS villages (
    village_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

ALTER TABLE customers
    ADD COLUMN IF NOT EXISTS address_id INT NULL,
    ADD COLUMN IF NOT EXISTS village_id INT NULL,
    ADD COLUMN IF NOT EXISTS entry_date DATE NULL;

-- From database/migrate.py
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s

SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND column_name = %s

CREATE TABLE addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    address TEXT
)

CREATE TABLE villages (
    village_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)

ALTER TABLE customers ADD COLUMN address_id INT NULL

ALTER TABLE customers ADD COLUMN village_id INT NULL

ALTER TABLE customers ADD COLUMN entry_date DATE NULL

ALTER TABLE items ADD COLUMN interest_type VARCHAR(20) DEFAULT 'PERCENT' NULL
ALTER TABLE items ADD COLUMN serial_no VARCHAR(255) NULL
ALTER TABLE items ADD COLUMN invoice_no VARCHAR(255) NULL
ALTER TABLE items ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE' NULL

-- From models/village_model.py
INSERT INTO villages (name) VALUES (%s)

SELECT * FROM villages ORDER BY name

SELECT * FROM villages WHERE village_id = %s

-- From models/report_model.py
SELECT
    c.customer_id,
    c.name,
    c.phone,
    c.address,
    i.item_id,
    i.brand,
    i.model,
    i.item_amount,
    i.total_installments,
    IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0) AS total_paid,
    (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) AS due_amount,
    CASE WHEN (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) <= 0 THEN 'Paid' ELSE 'Unpaid' END AS paid_status,
    v.name AS village_name,
    (SELECT MAX(payment_date) FROM payments p2 WHERE p2.item_id = i.item_id) AS last_payment_date
FROM customers c
LEFT JOIN items i ON c.customer_id = i.customer_id
LEFT JOIN villages v ON c.village_id = v.village_id
WHERE 1=1

AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) <= 0

AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) > 0

AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) >= %s

AND (COALESCE(i.item_amount, 0) - IFNULL((SELECT SUM(p.amount_paid) FROM payments p WHERE p.item_id = i.item_id), 0)) <= %s

AND EXISTS (SELECT 1 FROM payments p3 WHERE p3.item_id = i.item_id AND p3.payment_date >= %s)

AND EXISTS (SELECT 1 FROM payments p4 WHERE p4.item_id = i.item_id AND p4.payment_date <= %s)

-- From models/payment_model.py
SELECT remaining_amount FROM payments WHERE item_id = %s ORDER BY payment_date DESC LIMIT 1

INSERT INTO payments (
    item_id,
    amount_paid,
    payment_date,
    remaining_amount,
    remarks
) VALUES (%s, %s, %s, %s, %s)

SELECT * FROM payments WHERE item_id = %s ORDER BY payment_date

SELECT p.*, i.brand, i.model, i.item_amount, i.customer_id,
    c.name AS customer_name, c.phone AS customer_phone, c.address AS customer_address
FROM payments p
JOIN items i ON p.item_id = i.item_id
JOIN customers c ON i.customer_id = c.customer_id
ORDER BY p.payment_date DESC

-- From models/item_model.py
INSERT INTO items (
    customer_id,
    brand,
    model,
    item_amount,
    total_installments,
    interest_rate,
    interest_type,
    status
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

SELECT * FROM items WHERE customer_id = %s

SELECT * FROM items WHERE item_id = %s

UPDATE items SET status = %s WHERE item_id = %s

-- From models/guarantor_model.py
INSERT INTO guarantors (customer_id, name, phone, address) VALUES (%s, %s, %s, %s)

SELECT * FROM guarantors WHERE customer_id = %s

SELECT COUNT(*) FROM guarantors WHERE customer_id = %s

DELETE FROM guarantors WHERE guarantor_id = %s

-- From models/customer_model.py
INSERT INTO customers (name, phone, address, remarks, image_path, address_id, village_id, entry_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

SELECT c.*, v.name AS village_name, a.address AS address_text FROM customers c LEFT JOIN villages v ON c.village_id = v.village_id LEFT JOIN addresses a ON c.address_id = a.address_id ORDER BY c.customer_id DESC

SELECT c.*, v.name AS village_name, a.address AS address_text FROM customers c LEFT JOIN villages v ON c.village_id = v.village_id LEFT JOIN addresses a ON c.address_id = a.address_id WHERE c.customer_id = %s

UPDATE customers SET name=%s, phone=%s, address=%s, remarks=%s, address_id=%s, village_id=%s, entry_date=%s WHERE customer_id=%s

DELETE FROM customers WHERE customer_id = %s

INSERT INTO customers (name, phone, address, remarks, entry_date) VALUES (%s, %s, %s, %s, %s)

-- From models/address_model.py
INSERT INTO addresses (address) VALUES (%s)

SELECT * FROM addresses ORDER BY address

SELECT * FROM addresses WHERE address_id = %s
