
  
    

  create  table "data_warehouse"."public"."users__dbt_tmp"
  
  
    as
  
  (
    SELECT
    id,
    name,
    email,
    phone,
    created_at,
    updated_at
FROM "data_warehouse"."public"."users"
  );
  