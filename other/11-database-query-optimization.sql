-- Database Query Optimization Examples
-- Demonstrate slow queries and their optimized versions

-- ===========================
-- EXAMPLE 1: N+1 Query Problem
-- ===========================

-- SLOW: N+1 queries (1 + N queries)
-- This will execute 1 + number_of_users queries
-- Prompt: Optimize this N+1 query pattern

SELECT * FROM orders WHERE user_id = ?;  -- Execute once per user

-- OPTIMIZED: Single query with JOIN
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';


-- ===========================
-- EXAMPLE 2: Missing Index
-- ===========================

-- SLOW: Full table scan
-- Prompt: Why is this query slow and how to optimize?

SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2023-01-01'
GROUP BY u.id, u.name;

-- OPTIMIZED: Add indexes
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Then the same query will use indexes instead of full table scans


-- ===========================
-- EXAMPLE 3: Subquery Optimization
-- ===========================

-- SLOW: Correlated subquery
-- Prompt: Make this query more efficient without using subqueries

SELECT p.id, p.name,
  (SELECT COUNT(*) FROM reviews r WHERE r.product_id = p.id) as review_count,
  (SELECT AVG(rating) FROM reviews r WHERE r.product_id = p.id) as avg_rating
FROM products p;

-- OPTIMIZED: Single query with GROUP BY and JOIN
SELECT p.id, p.name, COUNT(r.id) as review_count, AVG(r.rating) as avg_rating
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name;


-- ===========================
-- EXAMPLE 4: UNION vs UNION ALL
-- ===========================

-- SLOW: Removes duplicates (expensive operation)
-- Prompt: Optimize this UNION query

SELECT user_id, 'order' as type FROM orders
UNION
SELECT user_id, 'review' as type FROM reviews;

-- OPTIMIZED: If duplicates are acceptable
SELECT user_id, 'order' as type FROM orders
UNION ALL
SELECT user_id, 'review' as type FROM reviews;


-- ===========================
-- EXAMPLE 5: Aggregation Optimization
-- ===========================

-- SLOW: Unnecessary columns in GROUP BY
-- Prompt: Optimize this aggregation query

SELECT u.id, u.name, u.email, u.phone, u.address, 
       COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email, u.phone, u.address;

-- OPTIMIZED: Only group by necessary columns
SELECT u.id, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Then JOIN back if you need other columns
-- Or use window functions if available


-- ===========================
-- EXAMPLE 6: Window Functions
-- ===========================

-- SLOW: Multiple self-joins for ranking
-- Prompt: How can I efficiently rank products by sales?

SELECT p.id, p.name, COUNT(o.id) as sales
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
GROUP BY p.id, p.name
ORDER BY sales DESC
LIMIT 10;

-- OPTIMIZED: Use window functions
SELECT DISTINCT p.id, p.name, sales,
  ROW_NUMBER() OVER (ORDER BY sales DESC) as rank
FROM (
  SELECT p.id, p.name, COUNT(o.id) as sales
  FROM products p
  LEFT JOIN order_items oi ON p.id = oi.product_id
  LEFT JOIN orders o ON oi.order_id = o.id
  GROUP BY p.id, p.name
) ranked
LIMIT 10;
