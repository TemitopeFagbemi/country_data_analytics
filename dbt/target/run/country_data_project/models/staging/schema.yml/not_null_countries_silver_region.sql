
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select region
from COUNTRY_DB.PUBLIC.countries_silver
where region is null



  
  
      
    ) dbt_internal_test