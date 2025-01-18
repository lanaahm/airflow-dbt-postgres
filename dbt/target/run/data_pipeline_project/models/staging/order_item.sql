
  
    

  create  table "data_warehouse"."public"."order_item__dbt_tmp"
  
  
    as
  
  (
    SELECT
    id,
    order_id,
    goods_id,
    qty,
    created_at,
    updated_at
FROM "data_warehouse"."public"."order_item"
  );
  