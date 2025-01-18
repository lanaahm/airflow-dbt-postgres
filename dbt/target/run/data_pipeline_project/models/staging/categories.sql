
  
    

  create  table "data_warehouse"."public"."categories__dbt_tmp"
  
  
    as
  
  (
    SELECT
    id,
    name,
    created_at,
    updated_at
FROM "data_warehouse"."public"."categories"
  );
  