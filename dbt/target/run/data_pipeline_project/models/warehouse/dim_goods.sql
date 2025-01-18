
  
    

  create  table "data_warehouse"."public"."dim_goods__dbt_tmp"
  
  
    as
  
  (
    SELECT
    *
FROM "data_warehouse"."public"."goods"
  );
  