-- schema.sql
-- 1. Reset Environment
DROP TABLE IF EXISTS orders CASCADE;

-- 2. Create Target Schema
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL
);

-- 3. Seed 1 Million Rows using generate_series
INSERT INTO orders (id, user_id, status, metadata, created_at)
SELECT 
    g.id,
    (floor(random() * 50000) + 1)::INT AS user_id,
    (ARRAY['pending', 'completed', 'shipped', 'cancelled'])[floor(random() * 4 + 1)] AS status,
    jsonb_build_object(
        'tier', (ARRAY['gold', 'silver', 'bronze'])[floor(random() * 3 + 1)],
        'ip', '192.168.1.' || floor(random() * 255)::text
    ) AS metadata,
    NOW() - (random() * interval '365 days') AS created_at
FROM generate_series(1, 1000000) AS g(id);

-- 4. Analyze Table Metadata for Planner
VACUUM ANALYZE orders;