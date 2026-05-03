
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select currency_code
from COUNTRY_DB.PUBLIC.countries_silver
where currency_code is null



  
  
      
    ) dbt_internal_test