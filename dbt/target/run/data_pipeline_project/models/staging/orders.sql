
  
    

  create  table "data_warehouse"."public"."orders__dbt_tmp"
  
  
    as
  
  (
    SELECT
    id,
    user_id,
    is_refund,
    created_at,
    updated_at
FROM "data_warehouse"."public"."orders"
  );
  