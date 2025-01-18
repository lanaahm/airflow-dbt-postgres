
  
    

  create  table "data_warehouse"."public"."fact_transactions__dbt_tmp"
  
  
    as
  
  (
    WITH fact_base AS (
    SELECT
        o.user_id AS user_id,
        u.name AS user_name,
        oi.id AS order_item_id,
        oi.qty AS number_of_items_ordered,
        oi.qty * g.price AS total_purchase_value,
        o.created_at AS order_date
    FROM "data_warehouse"."public"."order_item" oi
    JOIN "data_warehouse"."public"."goods" g ON oi.goods_id = g.id
    JOIN "data_warehouse"."public"."orders" o ON oi.order_id = o.id
    JOIN "data_warehouse"."public"."users" u ON o.user_id = u.id
)
SELECT * FROM fact_base
  );
  