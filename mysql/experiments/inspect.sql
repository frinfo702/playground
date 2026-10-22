-- Look inside the server. Run: bin/sql < experiments/inspect.sql

-- Table and index sizes on disk.
SELECT table_name, table_rows,
       ROUND(data_length  / 1024 / 1024, 1) AS data_mb,
       ROUND(index_length / 1024 / 1024, 1) AS index_mb
FROM information_schema.tables WHERE table_schema = DATABASE();

-- Buffer pool: how much of the data is cached in memory.
SELECT pool_size, free_buffers, database_pages, hit_rate
FROM information_schema.innodb_buffer_pool_stats;

-- Which tables occupy the buffer pool right now.
SELECT object_name, allocated, pages FROM sys.innodb_buffer_stats_by_table
WHERE object_schema = DATABASE();

-- Heaviest statements so far (normalized), from performance_schema.
SELECT LEFT(query, 80) AS query, exec_count, total_latency, rows_examined_avg
FROM sys.statement_analysis WHERE db = DATABASE() LIMIT 10;
