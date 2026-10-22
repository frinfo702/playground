SET SESSION cte_max_recursion_depth = 1000000;

INSERT INTO users (name, email, country, created_at)
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM seq WHERE n < 10000)
SELECT CONCAT('user', n), CONCAT('user', n, '@example.com'),
       ELT(1 + n % 5, 'JP', 'US', 'DE', 'FR', 'BR'),
       '2024-01-01' + INTERVAL n MINUTE
FROM seq;

INSERT INTO orders (user_id, amount, status, created_at)
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM seq WHERE n < 200000)
SELECT 1 + FLOOR(RAND(n) * 10000), ROUND(RAND(n + 1) * 500, 2),
       ELT(1 + n % 4, 'pending', 'paid', 'shipped', 'cancelled'),
       '2024-01-01' + INTERVAL FLOOR(RAND(n + 2) * 365 * 24 * 60) MINUTE
FROM seq;

INSERT INTO accounts VALUES (1, 'alice', 1000), (2, 'bob', 1000);
ANALYZE TABLE users, orders, accounts;
