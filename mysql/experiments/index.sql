-- How an index changes the plan. Run: bin/sql < experiments/index.sql
-- Watch "type", "rows", and the actual time in EXPLAIN ANALYZE.

-- 1) No index on created_at -> full table scan (type=ALL, ~200k rows).
EXPLAIN SELECT COUNT(*) FROM orders WHERE created_at >= '2024-12-01';
EXPLAIN ANALYZE SELECT COUNT(*) FROM orders WHERE created_at >= '2024-12-01';

-- 2) With an index -> range scan over a fraction of the rows.
CREATE INDEX idx_created ON orders (created_at);
EXPLAIN SELECT COUNT(*) FROM orders WHERE created_at >= '2024-12-01';
EXPLAIN ANALYZE SELECT COUNT(*) FROM orders WHERE created_at >= '2024-12-01';

-- 3) Wrapping the column in a function defeats the range scan (type=index: reads all 200k entries).
EXPLAIN SELECT COUNT(*) FROM orders WHERE YEAR(created_at) = 2024 AND MONTH(created_at) = 12;

-- 4) Covering index: every needed column is in the index -> "Using index", no table lookups.
EXPLAIN SELECT user_id FROM orders WHERE user_id = 42;
EXPLAIN SELECT user_id, amount FROM orders WHERE user_id = 42;

DROP INDEX idx_created ON orders;
