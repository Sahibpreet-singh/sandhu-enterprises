-- Migration: add addresses and villages tables, add columns to customers

CREATE TABLE IF NOT EXISTS addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    address TEXT
);

CREATE TABLE IF NOT EXISTS villages (
    village_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

-- Add foreign key columns to customers table (run only if your DB version allows)
ALTER TABLE customers
    ADD COLUMN IF NOT EXISTS address_id INT NULL,
    ADD COLUMN IF NOT EXISTS village_id INT NULL,
    ADD COLUMN IF NOT EXISTS entry_date DATE NULL;

-- -- Optionally add FK constraints (uncomment if desired and supported)
-- ALTER TABLE customers
--     ADD CONSTRAINT fk_customers_address FOREIGN KEY (address_id) REFERENCES addresses(address_id),
--     ADD CONSTRAINT fk_customers_village FOREIGN KEY (village_id) REFERENCES villages(village_id);

-- Note: MySQL versions older than 8.0 do not support ADD COLUMN IF NOT EXISTS syntax.
-- If your server doesn't support it, run these commands manually after checking existing schema:
-- ALTER TABLE customers ADD COLUMN address_id INT NULL;
-- ALTER TABLE customers ADD COLUMN village_id INT NULL;
