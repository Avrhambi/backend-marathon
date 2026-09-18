-- run_benchmarks.sql
\pset pager off
\echo '==================================================='
\echo ' BENCHMARK 1: Baseline Query (No Index - Seq Scan)'
\echo '==================================================='
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT id, status, created_at 
FROM orders 
WHERE user_id = 12345 AND status = 'completed';

\echo '---------------------------------------------------'
\echo ' Creating Composite Index: idx_orders_user_status'
\echo '---------------------------------------------------'
CREATE INDEX idx_orders_user_status ON orders (user_id, status);

\echo '==================================================='
\echo ' BENCHMARK 2: Composite Index (Bitmap/Index Scan)'
\echo '==================================================='
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT id, status, created_at 
FROM orders 
WHERE user_id = 12345 AND status = 'completed';

\echo '---------------------------------------------------'
\echo ' Creating Covering Index: idx_orders_covering'
\echo '---------------------------------------------------'
CREATE INDEX idx_orders_covering ON orders (user_id, status) INCLUDE (created_at);

\echo '==================================================='
\echo ' BENCHMARK 3: Covering Index (Index-Only Scan)'
\echo '==================================================='
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT user_id, status, created_at 
FROM orders 
WHERE user_id = 12345 AND status = 'completed';

\echo '---------------------------------------------------'
\echo ' BENCHMARK 4: JSONB Query (No GIN Index)'
\echo '---------------------------------------------------'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT count(*) FROM orders WHERE metadata @> '{"tier": "gold"}';

\echo '---------------------------------------------------'
\echo ' Creating GIN Index: idx_orders_metadata_gin'
\echo '---------------------------------------------------'
CREATE INDEX idx_orders_metadata_gin ON orders USING gin (metadata);

\echo '==================================================='
\echo ' BENCHMARK 5: JSONB Query with GIN Index'
\echo '==================================================='
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT count(*) FROM orders WHERE metadata @> '{"tier": "gold"}';