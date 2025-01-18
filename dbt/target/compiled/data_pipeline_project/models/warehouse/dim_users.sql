SELECT
    u.id AS user_id,
    u.name,
    u.email,
    u.phone,
    MAX(o.updated_at) AS last_transaction
FROM "data_warehouse"."public"."users" AS u
LEFT JOIN "data_warehouse"."public"."orders" AS o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email, u.phone