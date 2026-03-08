-- =============================================================
-- Sales Database Schema
-- Compatible with PostgreSQL 15+ and SQLite 3
-- =============================================================

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INTEGER PRIMARY KEY,
    first_name    TEXT    NOT NULL,
    last_name     TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    region        TEXT    NOT NULL,
    created_at    DATE    NOT NULL DEFAULT CURRENT_DATE
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    product_id    INTEGER PRIMARY KEY,
    product_name  TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    unit_price    NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0)
);

-- Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date    DATE    NOT NULL DEFAULT CURRENT_DATE,
    status        TEXT    NOT NULL DEFAULT 'pending'
                          CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled'))
);

-- Order line items
CREATE TABLE IF NOT EXISTS order_items (
    item_id       INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0)
);

-- =============================================================
-- Sample Data
-- =============================================================

INSERT INTO customers (customer_id, first_name, last_name, email, region, created_at) VALUES
(1, 'Alice',   'Smith',   'alice@example.com',   'North', '2023-01-10'),
(2, 'Bob',     'Jones',   'bob@example.com',     'South', '2023-02-14'),
(3, 'Carol',   'White',   'carol@example.com',   'East',  '2023-03-05'),
(4, 'David',   'Brown',   'david@example.com',   'West',  '2023-04-22'),
(5, 'Eva',     'Davis',   'eva@example.com',     'North', '2023-06-01');

INSERT INTO products (product_id, product_name, category, unit_price) VALUES
(1, 'Widget A', 'Widgets',  25.00),
(2, 'Widget B', 'Widgets',  40.00),
(3, 'Widget C', 'Widgets',  60.00),
(4, 'Gadget X', 'Gadgets', 120.00),
(5, 'Gadget Y', 'Gadgets',  85.00);

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
(1, 1, '2024-01-05', 'delivered'),
(2, 2, '2024-01-12', 'delivered'),
(3, 3, '2024-02-03', 'delivered'),
(4, 1, '2024-02-18', 'shipped'),
(5, 4, '2024-03-07', 'delivered'),
(6, 5, '2024-03-15', 'delivered'),
(7, 2, '2024-04-02', 'pending'),
(8, 3, '2024-04-20', 'delivered'),
(9, 4, '2024-05-11', 'delivered'),
(10,1, '2024-05-28', 'cancelled');

INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES
(1,  1, 1, 10, 25.00),
(2,  2, 2,  5, 40.00),
(3,  3, 1,  8, 25.00),
(4,  4, 3,  3, 60.00),
(5,  5, 2, 12, 40.00),
(6,  6, 1,  7, 25.00),
(7,  7, 3,  4, 60.00),
(8,  8, 2,  9, 40.00),
(9,  9, 1, 15, 25.00),
(10,10, 3,  6, 60.00),
(11, 1, 4,  2,120.00),
(12, 5, 5,  3, 85.00);
