
  
    

  create  table "data_warehouse"."public"."goods__dbt_tmp"
  
  
    as
  
  (
    SELECT
    id,
    category_id,
    name,
    price,
    created_at,
    updated_at
FROM "data_warehouse"."public"."goods"
  );
  