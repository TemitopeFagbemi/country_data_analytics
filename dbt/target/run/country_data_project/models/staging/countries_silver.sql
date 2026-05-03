-- back compat for old kwarg name
  
  begin;
    
        
            
	    
	    
            
        
    

    

    merge into COUNTRY_DB.PUBLIC.countries_silver as DBT_INTERNAL_DEST
        using COUNTRY_DB.PUBLIC.countries_silver__dbt_tmp as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.country_name = DBT_INTERNAL_DEST.country_name))

    
    when matched then update set
        "COUNTRY_NAME" = DBT_INTERNAL_SOURCE."COUNTRY_NAME","REGION" = DBT_INTERNAL_SOURCE."REGION","POPULATION" = DBT_INTERNAL_SOURCE."POPULATION","CAPITAL_CITY" = DBT_INTERNAL_SOURCE."CAPITAL_CITY","CURRENCY_CODE" = DBT_INTERNAL_SOURCE."CURRENCY_CODE","CURRENCY_NAME" = DBT_INTERNAL_SOURCE."CURRENCY_NAME","LOAD_TIMESTAMP" = DBT_INTERNAL_SOURCE."LOAD_TIMESTAMP"
    

    when not matched then insert
        ("COUNTRY_NAME", "REGION", "POPULATION", "CAPITAL_CITY", "CURRENCY_CODE", "CURRENCY_NAME", "LOAD_TIMESTAMP")
    values
        ("COUNTRY_NAME", "REGION", "POPULATION", "CAPITAL_CITY", "CURRENCY_CODE", "CURRENCY_NAME", "LOAD_TIMESTAMP")

;
    commit;