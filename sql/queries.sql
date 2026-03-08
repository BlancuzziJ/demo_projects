-- =============================================================
-- Sales Database – Analytical Queries
-- =============================================================

-- 1. Total revenue per region (delivered orders only)
SELECT
    c.region,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items  oi
JOIN orders       o  ON oi.order_id    = o.order_id
JOIN customers    c  ON o.customer_id  = c.customer_id
WHERE o.status = 'delivered'
GROUP BY c.region
ORDER BY total_revenue DESC;


-- 2. Top 3 products by revenue
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products    p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 3;


-- 3. Monthly revenue trend (all statuses except cancelled)
SELECT
    strftime('%Y-%m', o.order_date) AS month,   -- SQLite syntax
    -- DATE_TRUNC('month', o.order_date)         -- PostgreSQL syntax
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN orders      o ON oi.order_id = o.order_id
WHERE o.status <> 'cancelled'
GROUP BY month
ORDER BY month;


-- 4. Customer lifetime value (CLV) with ranking
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(DISTINCT o.order_id)         AS total_orders,
    SUM(oi.quantity * oi.unit_price)   AS lifetime_value,
    RANK() OVER (
        ORDER BY SUM(oi.quantity * oi.unit_price) DESC
    )                                  AS clv_rank
FROM customers   c
JOIN orders      o  ON c.customer_id  = o.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
WHERE o.status <> 'cancelled'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY clv_rank;


-- 5. Running total of revenue ordered by date (window function)
WITH daily_revenue AS (
    SELECT
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS daily_total
    FROM order_items oi
    JOIN orders      o ON oi.order_id = o.order_id
    WHERE o.status <> 'cancelled'
    GROUP BY o.order_date
)
SELECT
    order_date,
    daily_total,
    SUM(daily_total) OVER (ORDER BY order_date) AS running_total
FROM daily_revenue
ORDER BY order_date;


-- 6. Products that have never been ordered
SELECT p.product_id, p.product_name
FROM   products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE  oi.item_id IS NULL;
