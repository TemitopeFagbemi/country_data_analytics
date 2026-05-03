

SELECT
    data:name.common::STRING       AS country_name,
    data:region::STRING            AS region,
    data:population::NUMBER        AS population,
    data:capital[0]::STRING        AS capital_city,

    -- ✅ SAFE currency extraction
    CASE 
    WHEN data:currencies IS NOT NULL 
         AND ARRAY_SIZE(OBJECT_KEYS(data:currencies)) > 0
    THEN OBJECT_KEYS(data:currencies)[0]::STRING
    ELSE 'NO_CURRENCY'
END AS currency_code,

CASE 
    WHEN data:currencies IS NOT NULL 
         AND ARRAY_SIZE(OBJECT_KEYS(data:currencies)) > 0
    THEN data:currencies[OBJECT_KEYS(data:currencies)[0]].name::STRING
    ELSE 'NO_CURRENCY'
END AS currency_name,

    load_timestamp

FROM COUNTRY_DB.PUBLIC.countries_data_raw


WHERE load_timestamp > (
    SELECT MAX(load_timestamp) FROM COUNTRY_DB.PUBLIC.countries_silver
)


QUALIFY ROW_NUMBER() OVER (
    PARTITION BY country_name
    ORDER BY load_timestamp DESC
) = 1