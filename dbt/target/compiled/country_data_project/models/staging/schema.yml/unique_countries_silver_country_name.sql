
    
    

select
    country_name as unique_field,
    count(*) as n_records

from COUNTRY_DB.PUBLIC.countries_silver
where country_name is not null
group by country_name
having count(*) > 1


